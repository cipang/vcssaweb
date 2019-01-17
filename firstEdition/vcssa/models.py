import os
import smtplib

from django import forms
from django.db import models
from django.utils.datetime_safe import date
from modelcluster.fields import ParentalKey
from wagtail.admin.utils import send_mail
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList, \
    FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
import datetime

from firstEdition.settings import dev
from home.models import HomePage
from wagtail.contrib.settings.models import BaseSetting, register_setting

from modelcluster.fields import ParentalKey

from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel

#
# NUM_OF_SUBUNIONS = 8
# ANCESTOR_LEVEL = 2


class AboutPage(Page):
    show_in_menus_default = True
    intro = models.CharField(max_length=500, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('about_images', label="About images"),
    ]


class AboutPageGalleryImage(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name='about_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
    ]


class SubUnionIndexPage(Page):
    parent_page_types = ['home.HomePage']
    show_in_menus_default = True
    intro = models.CharField(max_length=500, blank=True)
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('intro'), ImageChooserPanel('background_image'), ]

    # get all published pages created by SubUnionHomePage template
    def get_context(self, request):
        context = super().get_context(request)
        subpages = SubUnionHomePage.objects.live()
        print(subpages)
        context['subunions'] = subpages
        return context


class SubUnionIndexPageGalleryImage(Orderable):
    page = ParentalKey(SubUnionIndexPage, on_delete=models.CASCADE, related_name='sub_union_images')
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
    ]


# page for a single sub union
class SubUnionHomePage(Page):
    parent_page_types = ['home.HomePage']

    # sub union name to be displayed on index page
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=500)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('intro'),
        ImageChooserPanel('logo'),
    ]


# activity index page (used to show all activities)
class ActivityIndexPage(Page):
    parent_page_types = ['home.HomePage', 'vcssa.SubUnionHomePage']
    show_in_menus_default = True
    intro = models.CharField(max_length=500, blank=True)

    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('background_image'),
        # InlinePanel('activity_index_images', label="Activity images"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        activities = self.get_children().live().order_by('-first_published_at')
        context['activities'] = activities
        return context


# activity index page images
# class ActivityIndexPageGalleryImage(Orderable):
#     page = ParentalKey(ActivityIndexPage, on_delete=models.CASCADE, related_name='activity_index_images')
#     image = models.ForeignKey(
#         'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
#     )
#     panels = [
#         ImageChooserPanel('image'),
#     ]


# activity page for a single activity
class ActivityPage(Page):
    # parent_page_types = ['ActivityIndexPage']
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=500)
    date = models.DateField(("Date"), default=datetime.date.today)
    detail = RichTextField(blank=True)
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('intro'),
        FieldPanel('date'),
        FieldPanel('detail'),
        ImageChooserPanel('background_image'),
    ]


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL', null=True)
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram username, without the @')
    twitter = models.URLField(
        help_text='Your Facebook page URL', null=True)
    facebook_tab_panels = [
        FieldPanel('facebook'),
    ]
    instagram_tab_panels = [
        FieldPanel('instagram'),
    ]
    twitter_tab_panels = [
        FieldPanel('twitter'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(facebook_tab_panels, heading='First tab'),
        ObjectList(instagram_tab_panels, heading='Second tab'),
        ObjectList(twitter_tab_panels, heading='Third tab'),
    ])


class FormField(AbstractFormField):
    page = ParentalKey('ContactUsPage', related_name='form_fields')


class ContactUsPage(AbstractEmailForm):
    background_image = models.ForeignKey(
        'wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    intro_image = models.ForeignKey(
        'wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    intro = RichTextField(blank=True, default="Please contact us through our WeChat, or leave a message")
    thank_you_text = RichTextField(blank=True, default="Thank you for contacting us! We will get back to you soon.")
    email_password = models.CharField(max_length=16,default=None)

    facebook = models.URLField(blank=True, null=True, help_text='Your Facebook page URL')
    instagram = models.URLField(blank=True, max_length=255, help_text='Your Instagram page URL', null=True)
    weibo = models.URLField(blank=True, null=True, help_text='Your Weibo page URL')
    weChat = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+', help_text='Your WeChat QR Code')


    content_panels = [
        FieldPanel('title'),
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('background_image'),
        ImageChooserPanel('intro_image'),
        FieldPanel('facebook'),
        FieldPanel('instagram'),
        FieldPanel('weibo'),
        ImageChooserPanel('weChat'),

        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel(
            [
                FieldPanel('from_address', help_text="Please enter an email to send the message"),
                FieldPanel('email_password'),
                FieldPanel('to_address', help_text='Please enter an email to receive notifications'),
                FieldPanel('subject'),
            ],
            heading="Email Configuration",
        ),
    ]

    def send_mail(self, form):
        # dev.EMAIL_HOST_USER = self.from_address
        # dev.EMAIL_HOST_PASSWORD = self.email_password
        # print(dev.EMAIL_HOST_USER)
        # print(dev.EMAIL_HOST_PASSWORD)
        addresses = [address.strip() for address in self.to_address.split(',')]
        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))
        submitted_date_str = date.today().strftime('%x')
        content.append('{}: {}'.format('Submitted', submitted_date_str))
        content.append('{}: {}'.format('Submitted Via', self.full_url))
        content = '\n'.join(content)
        subject = self.subject + " - " + submitted_date_str
        send_mail(subject, content, addresses, self.from_address)
