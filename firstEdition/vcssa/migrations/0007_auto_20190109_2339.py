# Generated by Django 2.1.4 on 2019-01-09 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcssa', '0006_activitypage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitypage',
            name='intro',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='activitypage',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]