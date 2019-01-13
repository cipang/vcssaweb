# Generated by Django 2.1.4 on 2019-01-09 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailimages', '0021_image_file_hash'),
        ('vcssa', '0005_auto_20190109_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('intro', models.CharField(blank=True, max_length=500)),
                ('background_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
