# Generated by Django 2.1.5 on 2019-03-10 04:21

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20190310_1521'),
        ('wagtailimages', '0021_image_file_hash'),
        ('vcssa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subunionhomepage',
            name='logo',
        ),
        migrations.AddField(
            model_name='subunionhomepage',
            name='background_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subunion_background_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='subunionhomepage',
            name='index_pages',
            field=wagtail.core.fields.StreamField([('index_page', wagtail.core.blocks.PageChooserBlock(['vcssa.NewsPage', 'vcssa.ActivityPage'], null=True, required=False))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subunionhomepage',
            name='logo_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subunion_logo_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='subunionhomepage',
            name='posters',
            field=wagtail.core.fields.StreamField([('posters', wagtail.images.blocks.ImageChooserBlock())], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subunionhomepage',
            name='theme_background',
            field=models.ForeignKey(limit_choices_to={'type': 'HOME_BACKGROUND'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subunion_background_theme', to='home.Theme'),
        ),
        migrations.AddField(
            model_name='subunionhomepage',
            name='theme_news',
            field=models.ForeignKey(limit_choices_to={'type': 'HOME_NEWS'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subunion_news_theme', to='home.Theme'),
        ),
        migrations.AddField(
            model_name='subunionhomepage',
            name='theme_slide',
            field=models.ForeignKey(limit_choices_to={'type': 'HOME_SLIDE'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subunion_slide_theme', to='home.Theme'),
        ),
        migrations.AddField(
            model_name='subunionhomepage',
            name='welcome',
            field=models.CharField(default='Welcome!', max_length=200),
        ),
        migrations.AlterField(
            model_name='subunionhomepage',
            name='intro',
            field=models.CharField(default='The introduction of your union', help_text='Introduce your union here', max_length=255),
        ),
        migrations.AlterField(
            model_name='subunionhomepage',
            name='name',
            field=models.CharField(help_text='Enter your subunion name to be displayed on the index page.', max_length=100),
        ),
    ]
