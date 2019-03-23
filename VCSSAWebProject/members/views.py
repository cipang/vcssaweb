from urllib import parse
from urllib.parse import urljoin

from django import forms
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model, update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import EmailMessage
from django.db.models import Q, ManyToManyField
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseNotFound, QueryDict
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy, resolve
from django.utils.encoding import force_bytes, force_text, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.views.decorators.vary import vary_on_headers

from wagtail.admin import messages
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.utils import any_permission_required, permission_denied, permission_required
from wagtail.core import hooks
from wagtail.core.compat import AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME
from wagtail.users.forms import UserCreationForm, UserEditForm
from wagtail.users.utils import user_can_delete_user
from wagtail.utils.loading import get_custom_form
from wagtail.utils.pagination import paginate

from django.contrib.auth.models import Group
from itertools import chain
import urllib

from members.tokens import account_activation_token
from users.models import Subunions
from vcssa.models import ActivityPage
from vcssa.templatetags.global_tags import vcssa_home
from .forms import SignUpPage, SignInPage, EditProfilePage

COMMON_MAILS = {'gmail.com': 'https://mail.google.com/',
                'hotmail.com': 'https://outlook.live.com/',
                'outlook.com': 'https://outlook.live.com/',
                'live.com': 'https://outlook.live.com/',
                'msn.com': 'https://outlook.live.com/',
                'yahoo.com': 'https://mail.yahoo.com/',
                'qq.com': 'https://mail.qq.com/',
                '163.com': 'https://mail.163.com/',
                '126.com': 'https://www.126.com/',
                'sina.': 'https://mail.sina.com.cn/',
                'sohu.com': 'https://mail.sohu.com/',
                }

User = get_user_model()

# Typically we would check the permission 'auth.change_user' (and 'auth.add_user' /
# 'auth.delete_user') for user management actions, but this may vary according to
# the AUTH_USER_MODEL setting
add_user_perm = "{0}.add_{1}".format(AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower())
change_user_perm = "{0}.change_{1}".format(AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower())
delete_user_perm = "{0}.delete_{1}".format(AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower())

from django.shortcuts import render_to_response
from django.template import RequestContext


def handler404(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def get_email_host_link(to_email):
    host_link = None  # link to user's mailbox
    prefix, suffix = to_email.split("@")
    for mail in COMMON_MAILS:
        if suffix in mail:
            host_link = COMMON_MAILS[mail]
    return host_link


def send_validation_email(request, user, to_email, type):
    mail_subject = {'register': 'Activate your VCSSA account.',
                    'reset_password': 'Confirm your New Password.'}
    content = {'register': 'Please click on the link to confirm your registration: ',
               'reset_password': '[ Please ignore this email if it is not the action of yourself.]\n' +
                                 'You are receiving this email because you apply to change your password.\n' +
                                 'Please click on the link to confirm your action: ', }

    message = render_to_string('account_activation_email.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': account_activation_token.make_token(user),
        'content': content.get(type),
    })
    if message is not None and to_email is not None:
        print("sending email")
        email = EmailMessage(
            mail_subject.get(type), message, to=[to_email]
        )
        try:
            email.send()
            messages.success(request, 'Email sent successfully !')
            return True
        except:
            messages.error(request, "Could Not Send Email Due to Errors")
            return False


def signup(request):
    if request.method == 'POST':
        form = SignUpPage(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # for subunion in form.cleaned_data.get('subunions'):
            #     user.subunions.add(subunion)
            to_email = form.cleaned_data.get('email')
            if send_validation_email(request, user, to_email, 'register'):
                host_link = get_email_host_link(to_email)
                request.session['to_email'] = to_email
                request.session['host_link'] = host_link
                request.session['username'] = user.username
                return render(request, 'activate_account_popup.html', {'host_link': host_link})
    else:
        form = SignUpPage()
    return render(request, 'sign_up.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        # request.session['user'] = user
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        # if user already activated account
        if user.is_active:
            messages.error(request, 'Your account is already activated!')
            return redirect('members:account_home')
        #  if activation token is valid
        elif account_activation_token.check_token(user, token):
            print("activating...")
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Congratulations, you are our members now !")
            return redirect('members:account_home')
        # if token expires but user's inactive profile remains
        elif not account_activation_token.check_token(user, token):
            return HttpResponseNotFound("Sorry, your validation email has expired.")
            #  if user's inactive profile has been removed
    else:
        messages.error(request, 'Sorry, your registration has expired. Please sign up again')
        return redirect(reverse_lazy('members:signup'))


def resend(request):
    to_email = request.session.get('to_email')
    host_link = request.session.get('host_link')
    username = request.session.get('username')

    if username is not None:
        user = User.objects.get(username=username)
        if user is not None:
            #  if user account is already activated
            if user.is_active:
                messages.error(request, 'Your account is already activated!')
                return redirect('members:account_home')
            #  if user account is not activated yet and user's inactive profile remains in db
            else:
                if send_validation_email(request, user, to_email, 'register'):
                    # reload session
                    request.session['host_link'] = host_link
                    return render(request, 'activate_account_popup.html', {'host_link': host_link})
        #  if user's inactive profile is removed from db
        else:
            print('in 404')
            messages.error(request, 'Sorry, your registration has expired. Please sign up again')
        return redirect(reverse_lazy('members:signup'))
    else:
        messages.warning(request, "Invalid action")
        return render(request, 'activate_account_popup.html', {'host_link': host_link})


def signin(request):
    resend_email = False
    if request.method == "POST":
        form = SignInPage(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            login(request, user)
            #  if user is can access wagtail admin
            if user.has_perm('wagtailadmin.access_admin'):
                return redirect(reverse_lazy('wagtailadmin_home'))
            else:
                if request.META.get('HTTP_REFERER') == urljoin('http://{}'.format(get_current_site(request).domain),
                                                               str(reverse_lazy('members:signin'))):
                    return redirect(reverse_lazy('members:account_home'))
                #  return to previous page if redirect from pages other than sign in
                else:
                    return redirect(request.META.get('HTTP_REFERER'))
        else:
            #  if the account is inactive, provide a resend activation email link
            for errorlist in form.errors.as_data().values():
                if errorlist[0].code == 'inactive':
                    email = form.cleaned_data.get('email')
                    request.session['to_email'] = email
                    request.session['host_link'] = get_email_host_link(email)
                    request.session['username'] = User.objects.get(email=email).username
                    resend_email = True
    else:
        form = SignInPage()
    return render(request, 'sign_in.html', {'form': form, 'resend': resend_email})


@login_required
def accounthome(request):
    if request.user.is_authenticated:
        #  redirect to admin page for admins
        if request.user.has_perm('wagtailadmin.access_admin'):
            return redirect(reverse_lazy('wagtailadmin_home'))
        user = request.user
        profile = get_user_profile(request, user)
        favorites = user.favorite_activities.all()
        firstname = user.first_name
        return render_to_response('account_home.html',
                                  {'profile': profile, 'firstname': firstname, 'favorites': favorites})
    #  if user is not logged in
    else:
        messages.error(request, "Please login to your account.")
        return redirect(reverse_lazy('members:signin'))


@login_required
def get_user_profile(request, user):
    # subunion_display = "<li>VCSSA</li>"
    # subunions = user.subunions.all()
    # for subunion in subunions:
    #     subunion_display += "<li>" + subunion.name + "</li>"
    userinfo = {'Membership Number': "{:06d}".format(user.id).replace("", " ")[1: -1],
                'Username': user.username,
                'Email': user.email,
                'First Name': user.first_name,
                'Last Name': user.last_name,
                'Birthday': user.birthday,
                'Member of Unions': user.subunions}
    return userinfo


@login_required
def view_favorite_activities(request):
    activities = request.user.favorite_activities.all()
    return activities


@login_required
def edit_profile(request):
    if request.user.is_authenticated:
        if request.user.has_perm('wagtailadmin.access_admin'):
            return redirect('wagtailusers_users:edit')
        if request.method == 'POST':
            form = EditProfilePage(request.POST)
            if form.is_valid():
                user = request.user
                for field in form.changed_data:
                    # if field == 'subunions':
                    #     user.subunions.clear()
                    #     for subunion in form.cleaned_data.get('subunions'):
                    #         user.subunions.add(subunion)
                    # else:
                    setattr(user, field, form.cleaned_data.get(field))
                user.save()
                messages.success(request, "Profile updated successfully.")
                return redirect(reverse_lazy('members:account_home'))
        else:
            form = EditProfilePage()
        return render(request, 'account_profile_update.html', {'form': form})
    else:
        messages.error(request, "Please login to your account.")
        return redirect(reverse_lazy('members:signin'))

    # messages.success(request, _("User '{0}' updated.").format(user), buttons=[
    #     messages.button(reverse_lazy('members:edit_profile', args=(user.pk,)), _('Edit'))
    # ])


@login_required
def mark_activities(request, page_id):
    previous_page = request.META.get('HTTP_REFERER')
    activity = ActivityPage.objects.get(id=page_id)
    try:
        request.user.favorite_activities.add(activity)
        messages.success(request, "Activity saved successfully!")
    except:
        messages.error(request, "Cannot save this activity due to errors")
    return redirect(previous_page)


@login_required
def unmark_activities(request, page_id):
    previous_page = request.META.get('HTTP_REFERER')
    activity = ActivityPage.objects.get(id=page_id)
    try:
        request.user.favorite_activities.remove(activity)
        messages.success(request, "Activity removed successfully!")
    except:
        messages.error(request, "Cannot remove this activity due to errors")
    return redirect(previous_page)


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')
# return redirect(vcssa_home().url)
