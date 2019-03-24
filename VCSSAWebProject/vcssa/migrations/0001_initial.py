# Generated by Django 2.1.5 on 2019-02-07 23:56

import datetime
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        ('wagtailimages', '0021_image_file_hash'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('union_name', models.CharField(blank=True, default='', help_text='Enter your union name', max_length=500, null=True)),
                ('intro', models.CharField(blank=True, max_length=500)),
                ('background_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('theme', models.ForeignKey(limit_choices_to={'type': 'ABOUT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='about_theme', to='home.Theme')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AboutPageGalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.Image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='about_images', to='vcssa.AboutPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.CharField(blank=True, max_length=500)),
                ('background_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('theme_background', models.ForeignKey(limit_choices_to={'type': 'ACTIVITY_INDEX_BACKGROUND'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_index_background_theme', to='home.Theme')),
                ('theme_catalog', models.ForeignKey(limit_choices_to={'type': 'ACTIVITY_INDEX_CATALOG'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_index_catalog_theme', to='home.Theme')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ActivityPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(max_length=100)),
                ('intro', models.CharField(max_length=500)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('background_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('cover_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('theme', models.ForeignKey(limit_choices_to={'type': 'ACTIVITY'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_theme', to='home.Theme')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ContactUsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name='to address')),
                ('from_address', models.CharField(blank=True, max_length=255, verbose_name='from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='subject')),
                ('intro', wagtail.core.fields.RichTextField(blank=True, default='Please contact us through our WeChat, or leave a message')),
                ('thank_you_text', wagtail.core.fields.RichTextField(blank=True, default='Thank you for contacting us! We will get back to you soon.')),
                ('address', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('facebook', models.URLField(blank=True, help_text='Your Facebook page URL', null=True)),
                ('instagram', models.URLField(blank=True, help_text='Your Instagram page URL', max_length=255, null=True)),
                ('weibo', models.URLField(blank=True, help_text='Your Weibo page URL', null=True)),
                ('background_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('theme', models.ForeignKey(limit_choices_to={'type': 'CONTACT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_theme', to='home.Theme')),
                ('weChat', models.ForeignKey(blank=True, help_text='Your WeChat QR Code', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('default_value', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL')], max_length=16, verbose_name='field type')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='vcssa.ContactUsPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.CharField(blank=True, max_length=500)),
                ('background_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('theme_background', models.ForeignKey(limit_choices_to={'type': 'NEWS_INDEX_BACKGROUND'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news_index_background_theme', to='home.Theme')),
                ('theme_content', models.ForeignKey(limit_choices_to={'type': 'NEWS_INDEX_CONTENT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news_index_content_theme', to='home.Theme')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NewsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('author', models.CharField(blank=True, max_length=30, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('intro', models.CharField(blank=True, max_length=255, null=True)),
                ('body', wagtail.core.fields.RichTextField()),
                ('cover_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NewsPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='vcssa.NewsPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vcssa_newspagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsTagIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('theme', models.ForeignKey(limit_choices_to={'type': 'NEWS_TAGS_INDEX'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news_tag_index_theme', to='home.Theme')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SubUnionHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(max_length=100)),
                ('intro', models.CharField(max_length=500)),
                ('logo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SubUnionIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.CharField(blank=True, max_length=500)),
                ('background_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('theme_background', models.ForeignKey(limit_choices_to={'type': 'SUBUNION_INDEX_BACKGROUND'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subunion_index_background_theme', to='home.Theme')),
                ('theme_content', models.ForeignKey(limit_choices_to={'type': 'SUBUNION_INDEX_CONTENT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subunion_index_content_theme', to='home.Theme')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SubUnionIndexPageGalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_union_images', to='vcssa.SubUnionIndexPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newspage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='vcssa.NewsPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='newspage',
            name='theme',
            field=models.ForeignKey(limit_choices_to={'type': 'NEWS'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news_page_theme', to='home.Theme'),
        ),
    ]
