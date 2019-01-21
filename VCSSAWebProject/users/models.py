from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models import Q
from wagtail.admin.edit_handlers import *
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from django import forms


class User(AbstractUser):
    country = models.CharField(verbose_name='country', max_length=255)
    # groups = models.ManyToManyField(Group, limit_choices_to=Q(name="editor"))




@register_setting
class SubunionUser(BaseSetting):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True )
    group = models.ManyToManyField(Group)

    panels = [
        FieldPanel('user.username'),
        FieldPanel('group', widget=forms.CheckboxSelectMultiple())
    ]





