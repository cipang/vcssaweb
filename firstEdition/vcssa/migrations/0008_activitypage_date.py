# Generated by Django 2.1.4 on 2019-01-10 00:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcssa', '0007_auto_20190109_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitypage',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
