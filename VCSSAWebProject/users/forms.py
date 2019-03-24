from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.settings.registry import register_setting

from wagtail.users.forms import UserEditForm, UserCreationForm, standard_fields, custom_fields

from members.forms import SignUpPage, EditProfilePage
from users.models import User, Subunions


class CustomUserEditForm(EditProfilePage):

    def __init__(self, *args, **kwargs):
        super(EditProfilePage, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].required = False
        self.fields.pop('is_superuser')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'birthday', 'subunions', 'groups', 'is_active')
        exclude = ('is_superuser',)
        widgets = {
            'groups': forms.CheckboxSelectMultiple
        }

    # class Meta:
    #     widgets = {
    #         'groups': forms.CheckboxSelectMultiple
    #     }
    # def auto_select_group(request):
    #     current_user = request.user
    #     print(current_user)
    #     print(request.user.groups)
    #
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #
    #     if self.password_enabled:
    #         password = self.cleaned_data['password1']
    #         if password:
    #             user.set_password(password)
    #
    #     if commit:
    #         user.save()
    #         self.save_m2m()
    #     return user


class CustomUserCreationForm(SignUpPage):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'birthday', 'subunions', 'groups', 'is_active')
        exclude = ('is_superuser',)
        widgets = {
            'groups': forms.CheckboxSelectMultiple
        }







