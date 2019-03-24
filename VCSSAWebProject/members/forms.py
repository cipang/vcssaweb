import datetime
import re

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserChangeForm
from django.forms import fields
from wagtail.users.forms import UserCreationForm, UserForm, UserEditForm

from users.models import User, Subunions

VALID_BIRTHDAY_FROM = datetime.date(1900, 1, 1)
VALID_BIRTHDAY_TO = datetime.date.today()


class SignUpPage(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpPage, self).__init__(*args, **kwargs)
        for fields in self.Meta.exclude:
            if fields in self.fields:
                del self.fields[fields]

    email = forms.EmailField(required=True, help_text="In order to provide a better community environment, "
                                                      "please enter your university email.")
    birthday = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    subunions = forms.ModelChoiceField(queryset=Subunions.objects.all(), required=False,
                                       widget=forms.Select, empty_label=None)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'birthday', 'subunions',)
        exclude = ('is_superuser',)

    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if birthday < VALID_BIRTHDAY_FROM or birthday > VALID_BIRTHDAY_TO:
            raise forms.ValidationError("Please enter a valid birthday.")
        return birthday

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not re.search("(\.edu|@vcssa.com.au)", email):
            raise forms.ValidationError("Please use your university email to register.")
        return email


class SignInPage(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Email does not exist! Please double check or Sign up.")
        return email

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.is_active:
                raise forms.ValidationError("Please activate your account to log in.", code='inactive')
            if authenticate(username=user.username, password=password) is None:
                raise forms.ValidationError("The email and password does not match.")
        return self.cleaned_data


class EditProfilePage(UserEditForm):
    def __init__(self, *args, **kwargs):
        super(EditProfilePage, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].required = False
        self.fields.pop('username')
        self.fields.pop('is_superuser')
        self.fields.pop('email')

    birthday = fields.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    subunions = forms.ModelChoiceField(queryset=Subunions.objects.all(), required=False, widget=forms.Select,
                                       empty_label=None)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'birthday', 'subunions', 'password1', 'password2')

    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if birthday is not None:
            if birthday < VALID_BIRTHDAY_FROM or birthday > VALID_BIRTHDAY_TO:
                raise forms.ValidationError("Please enter a valid birthday.")
        return birthday

# class PassWordResetForm():
#     pass
