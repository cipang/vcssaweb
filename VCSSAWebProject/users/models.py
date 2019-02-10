from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models import Q
from wagtail.admin.edit_handlers import *
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from django import forms
from django.utils.translation import ugettext_lazy as _


"""Only refers to the subunion of members to receive promotions.
   For editors, use 'Group' to restrict permissions"""
class Subunions(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=False, unique=True, error_messages={
        'unique': _("The email has already been registered."),
    },)
    birthday = models.DateField(blank=True, default="2000-1-1")
    subunions = models.ManyToManyField(Subunions, blank=True)



