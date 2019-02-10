# Generated by Django 2.1.4 on 2019-02-01 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vcssa', '0002_auto_20190201_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpage',
            name='theme',
            field=models.ForeignKey(limit_choices_to={'type': 'ABOUT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='about_theme', to='home.Theme'),
        ),
    ]
