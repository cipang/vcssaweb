from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.settings.registry import register_setting

from wagtail.users.forms import UserEditForm, UserCreationForm, standard_fields, custom_fields
from .models import SubunionUser


class CustomUserEditForm(UserEditForm):
    country = forms.CharField(required=True, label=_("Country"))
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





class CustomUserCreationForm(UserCreationForm):
    country = forms.CharField(required=True, label=_("Country"))


class SubUnionUserCreationForm(UserCreationForm):
    country = forms.CharField(required=True, label=_("Country"))




