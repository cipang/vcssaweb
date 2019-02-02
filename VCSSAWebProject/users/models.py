from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models import Q
from wagtail.admin.edit_handlers import *
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from django import forms

"""Only refers to the subunion of members to receive promotions.
   For editors, use 'Group' to restrict permissions"""
class Subunions(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractUser):
    subunions = models.ManyToManyField(Subunions, blank=True)




