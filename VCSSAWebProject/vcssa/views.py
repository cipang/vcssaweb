from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from django.db import models

#
# @receiver(models.signals.post_save, sender=User)
# def post_save_user_signal_handler(sender, instance, created, **kwargs):
#     if created:
#         instance.is_staff = True
#         group = Group.objects.get(name='Group name')
#         instance.groups.add(group)
#         instance.save()