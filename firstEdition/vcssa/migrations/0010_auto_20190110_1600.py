# Generated by Django 2.1.4 on 2019-01-10 05:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('wagtailcore', '0040_page_draft_title'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('vcssa', '0009_subunionpage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubUnionPage',
            new_name='SubUnionHomePage',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_1_intro',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_1_logo',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_1_name',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_2_intro',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_2_logo',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_2_name',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_3_intro',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_3_logo',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_3_name',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_4_intro',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_4_logo',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_4_name',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_5_intro',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_5_logo',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_5_name',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_6_intro',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_6_logo',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_6_name',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_7_intro',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_7_logo',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_7_name',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_8_intro',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_8_logo',
        ),
        migrations.RemoveField(
            model_name='subunionindexpage',
            name='subunion_8_name',
        ),
    ]
