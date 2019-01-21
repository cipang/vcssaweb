# Generated by Django 2.1.4 on 2019-01-21 02:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailmenus', '0022_auto_20170913_2125'),
        ('wagtailcore', '0040_page_draft_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vcssa', '0007_blogtagindexpage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogTagIndexPage',
            new_name='NewsTagIndexPage',
        ),
    ]
