# Generated by Django 2.1.4 on 2019-01-10 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('vcssa', '0010_auto_20190110_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='subunionindexpage',
            name='background_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
