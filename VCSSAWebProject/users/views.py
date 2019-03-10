import re

from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
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

from django.contrib.auth.models import Group, Permission
from itertools import chain

from users.models import Subunions

User = get_user_model()
# VCSSA_ADMIN_GROUPNAME = "VCSSAAdmin"
# VCSSA_EDITOR_GROUPNAME = "VCSSAEditor"
ADMIN_GROUPNAME = ["VCSSAAdmin", "UnimelbAdmin", "MonashAdmin"]
EDITOR_GROUPNAME = {ADMIN_GROUPNAME[0]: "VCSSAEditor", ADMIN_GROUPNAME[1]: "UnimelbEditor",
                    ADMIN_GROUPNAME[2]: "MonashEditor"}

# Typically we would check the permission 'auth.change_user' (and 'auth.add_user' /
# 'auth.delete_user') for user management actions, but this may vary according to
# the AUTH_USER_MODEL setting
add_user_perm = "{0}.add_{1}".format(AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower())
change_user_perm = "{0}.change_{1}".format(AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower())
delete_user_perm = "{0}.delete_{1}".format(AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower())


def get_user_creation_form():
    form_setting = 'WAGTAIL_USER_CREATION_FORM'
    if hasattr(settings, form_setting):
        return get_custom_form(form_setting)
    else:
        return UserCreationForm


def get_user_edit_form():
    form_setting = 'WAGTAIL_USER_EDIT_FORM'
    if hasattr(settings, form_setting):
        return get_custom_form(form_setting)
    else:
        return UserEditForm


@any_permission_required(add_user_perm, change_user_perm, delete_user_perm)
@vary_on_headers('X-Requested-With')
def index(request):
    q = None
    is_searching = False

    model_fields = [f.name for f in User._meta.get_fields()]

    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder=_("Search users"))
        if form.is_valid():
            q = form.cleaned_data['q']
            is_searching = True
            conditions = Q()

            for term in q.split():
                if 'username' in model_fields:
                    conditions |= Q(username__icontains=term)

                if 'first_name' in model_fields:
                    conditions |= Q(first_name__icontains=term)

                if 'last_name' in model_fields:
                    conditions |= Q(last_name__icontains=term)

                if 'email' in model_fields:
                    conditions |= Q(email__icontains=term)

            users = User.objects.filter(conditions)
    else:
        form = SearchForm(placeholder=_("Search users"))

    if not is_searching:
        users = User.objects.all()

    if 'last_name' in model_fields and 'first_name' in model_fields:
        users = users.order_by('last_name', 'first_name')

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering == 'username':
            users = users.order_by(User.USERNAME_FIELD)
    else:
        ordering = 'name'

    """Display all users to superuser, users from the same union to admin"""
    # if not request.user.is_superuser:
    #     current_user_group = request.user.groups.all()
    #     for group in current_user_group:
    #         if group.name in ADMIN_GROUPNAME:
    #             group = Group.objects.filter(Q(name=group.name) | Q(name=EDITOR_GROUPNAME.get(group.name)))
    #             temp = None
    #             for item in group:
    #                 user = users.filter(groups=item)
    #                 if temp != None:
    #                     user = user | temp
    #                 temp = user
    #     users = user

    if not request.user.is_superuser:
        current_user_group = request.user.groups.all()
        if current_user_group:
            for group in current_user_group:
                if "Admin" in group.name:
                    try:
                        group = Group.objects.filter(Q(name=group.name) |
                                                     Q(name=group.name.replace("Admin", "Editor")) |
                                                     Q(name=group.name.replace("Admin", "Member")))
                        temp = None
                        for item in group:
                            user = users.filter(groups=item)
                            if temp != None:
                                user = user | temp
                            temp = user
                    except:
                        messages.error(request, "Cannot find any group in your Subunion")
            users = user

    paginator, users = paginate(request, users)

    if request.is_ajax():
        return render(request, "wagtailusers/users/results.html", {
            'users': users,
            'is_searching': is_searching,
            'query_string': q,
            'ordering': ordering,
        })
    else:
        return render(request, "wagtailusers/users/index.html", {
            'search_form': form,
            'users': users,
            'is_searching': is_searching,
            'ordering': ordering,
            'query_string': q,
        })


@permission_required(add_user_perm)
def create(request):
    """Return context to create.html"""
    is_admin = False
    is_superuser = request.user.is_superuser
    if 'wagtailadmin.union_admin' in request.user.get_all_permissions():
        is_admin = True

    # request_user_groups = request.user.groups.all()
    # print(request_user_groups)

    # usergroups = request.user.groups.all()
    # print(usergroups)
    # for name in ADMIN_GROUPNAME:
    #     print(name)
    #     for groupname in usergroups:
    #         if name == groupname.name:
    #             admin = True
    #             print("Admin")
    # if request.user.is_superuser:
    #     superuser = True
    #     print("Superuser")

    for fn in hooks.get_hooks('before_create_user'):
        result = fn(request)
        if hasattr(result, 'status_code'):
            return result

    if request.method == 'POST':
        form = get_user_creation_form()(request.POST, request.FILES)
        if form.is_valid():
            print('form valid')
            """Handle the setting views of different groups of users"""
            user = form.save()
            for group in request.user.groups.all():
                # If user is admin, add user as editor of corresponding union
                if group.permissions.filter(codename='union_admin'):
                    try:
                        user.groups.add(Group.objects.get(name=group.name.replace("Admin", "Editor")))
                    except:
                        messages.error(request, "Cannot add the new user to the editor group of your union")
            print(user.groups.all())

            messages.success(request, _("User '{0}' created.").format(user), buttons=[
                messages.button(reverse('wagtailusers_users:edit', args=(user.pk,)), _('Edit'))
            ])
            for fn in hooks.get_hooks('after_create_user'):
                result = fn(request, user)
                if hasattr(result, 'status_code'):
                    return result
            return redirect('wagtailusers_users:index')
        else:
            messages.error(request, _("The user could not be created due to errors."))
    else:
        form = get_user_creation_form()()

    print(is_admin)
    return render(request, 'wagtailusers/users/create.html',
                  {'form': form, 'is_admin': is_admin, 'is_superuser': is_superuser})


@permission_required(change_user_perm)
def edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    can_delete = user_can_delete_user(request.user, user)
    editing_self = request.user == user
    previous_groups = user.groups.all()
    previous_subunion = user.subunions
    print(previous_subunion)
    print(previous_groups)
    for fn in hooks.get_hooks('before_edit_user'):
        result = fn(request, user)
        if hasattr(result, 'status_code'):
            return result
    if request.method == 'POST':
        form = get_user_edit_form()(request.POST, request.FILES, instance=user, editing_self=editing_self)
        if form.is_valid():
            user = form.save()
            if 'wagtailadmin.union_admin' in request.user.get_all_permissions():
                user.subunions = previous_subunion
                if previous_groups:
                    for item in previous_groups:
                        user.groups.add(item)
                user.save()
            if user == request.user and 'password1' in form.changed_data:
                # User is changing their own password; need to update their session hash
                update_session_auth_hash(request, user)

            messages.success(request, _("User '{0}' updated.").format(user), buttons=[
                messages.button(reverse('wagtailusers_users:edit', args=(user.pk,)), _('Edit'))
            ])
            for fn in hooks.get_hooks('after_edit_user'):
                result = fn(request, user)
                if hasattr(result, 'status_code'):
                    return result
            return redirect('wagtailusers_users:index')
        else:
            messages.error(request, _("The user could not be saved due to errors."))
    else:
        form = get_user_edit_form()(instance=user, editing_self=editing_self)

    return render(request, 'wagtailusers/users/edit.html', {
        'user': user,
        'form': form,
        'can_delete': can_delete,
        'superuser': request.user.is_superuser
    })
