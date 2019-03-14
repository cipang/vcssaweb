import os
import smtplib

from django import forms
from django.contrib import messages
from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django.utils.datetime_safe import date
from django.utils.html import strip_tags
from modelcluster.fields import ParentalKey
from wagtail.admin.utils import send_mail
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList, \
    FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
import datetime

from wagtail.embeds.blocks import EmbedBlock

from VCSSAWebProject.settings import dev
from home.models import HomePage, RadioSelectWithPicture, Theme, THEME_CHOICES
from wagtail.contrib.settings.models import BaseSetting, register_setting

from modelcluster.fields import ParentalKey

from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock

from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

#
# NUM_OF_SUBUNIONS = 8
# ANCESTOR_LEVEL = 2

CONTACT_PAGE_FORM_FIELD_CHOICES = (
    ('singleline', _('Single line text')),
    ('multiline', _('Multi-line text')),
    ('email', _('Email')),
    ('number', _('Number')),
    ('url', _('URL')),
)


class AboutPage(Page):
    parent_page_types = ['home.HomePage', 'vcssa.SubUnionHomePage']
    subpage_types = []
    show_in_menus_default = True
    union_name = models.CharField(max_length=500, null=True, blank=True, default="", help_text="Enter your union name")
    intro = models.CharField(max_length=500, blank=True)
    background_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                              related_name="about_theme", limit_choices_to={'type': "ABOUT"})

    theme_panels = [
        FieldPanel('theme', widget=RadioSelectWithPicture),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('union_name'),
        ImageChooserPanel('background_image'),
        InlinePanel('about_images', label="About images"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request, *args, **kwargs):
        context = super(AboutPage, self).get_context(request, *args, **kwargs)
        context['theme'] = self.theme.template_path
        return context


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
    subpage_types = []
    show_in_menus_default = True
    intro = models.CharField(max_length=500, blank=True)
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    theme_background = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                         related_name="subunion_index_background_theme",
                                         limit_choices_to={'type': "SUBUNION_INDEX_BACKGROUND"})
    theme_content = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                      related_name="subunion_index_content_theme",
                                      limit_choices_to={'type': "SUBUNION_INDEX_CONTENT"})

    theme_panels = [
        FieldPanel('theme_background', widget=RadioSelectWithPicture),
        FieldPanel('theme_content', widget=RadioSelectWithPicture),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('intro'), ImageChooserPanel('background_image'), ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    # get all published pages created by SubUnionHomePage template
    def get_context(self, request):
        context = super().get_context(request)
        subpages = SubUnionHomePage.objects.live()
        print(subpages)
        context['subunions'] = subpages
        context['theme_background'] = self.theme_background.template_path
        context['theme_content'] = self.theme_content.template_path
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
    # sub union name to be displayed on index page
    name = models.CharField(max_length=100,
                            help_text="Enter your subunion name to be displayed on the index page.")
    parent_page_types = ['home.RootHomePage']
    subpage_types = ['vcssa.AboutPage', 'vcssa.SubUnionIndexPage', 'vcssa.ActivityIndexPage',
                     'vcssa.NewsIndexPage', 'vcssa.NewsTagIndexPage', 'vcssa.ContactUsPage']
    welcome = models.CharField(max_length=200, default="Welcome!")
    intro = models.CharField(max_length=255, default="The introduction of your union",
                             help_text="Introduce your union here")
    page_full_title = models.CharField(max_length=500, default="Victoria Chinese Student and Scholar Association",
                                       null=True, blank=True)
    background_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL,
                                         related_name='subunion_background_image')
    logo_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL,
                                   related_name='subunion_logo_image')
    posters = StreamField([('posters', ImageChooserBlock())], null=True, blank=True)
    index_pages = StreamField([
        ('index_page', blocks.PageChooserBlock(['vcssa.NewsPage', 'vcssa.ActivityPage'], null=True, required=False))
    ], null=True, blank=True)

    theme_background = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                         related_name="subunion_background_theme",
                                         limit_choices_to={'type': "HOME_BACKGROUND"})
    theme_slide = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                    related_name="subunion_slide_theme",
                                    limit_choices_to={'type': "HOME_SLIDE"})
    theme_news = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                   related_name="subunion_news_theme",
                                   limit_choices_to={'type': "HOME_NEWS"})
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('welcome'),
        FieldPanel('intro'),
        FieldPanel('page_full_title'),
        ImageChooserPanel('background_image'),
        ImageChooserPanel('logo_image'),
        StreamFieldPanel('posters'),
        StreamFieldPanel('index_pages'),
    ]

    theme_panels = [
        FieldPanel('theme_background', widget=RadioSelectWithPicture),
        FieldPanel('theme_slide', widget=RadioSelectWithPicture),
        FieldPanel('theme_news', widget=RadioSelectWithPicture),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request, *args, **kwargs):
        context = super(SubUnionHomePage, self).get_context(request, *args, **kwargs)
        context['background_theme'] = self.theme_background.template_path
        context['slide_theme'] = self.theme_slide.template_path
        context['news_theme'] = self.theme_news.template_path
        return context


# activity index page (used to show all activities)
class ActivityIndexPage(Page):
    parent_page_types = ['home.HomePage', 'vcssa.SubUnionHomePage']
    subpage_types = ['vcssa.ActivityPage']
    show_in_menus_default = True
    intro = models.CharField(max_length=500, blank=True)
    background_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    theme_background = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                         related_name="activity_index_background_theme",
                                         limit_choices_to={'type': "ACTIVITY_INDEX_BACKGROUND"})
    theme_catalog = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                      related_name="activity_index_catalog_theme",
                                      limit_choices_to={'type': "ACTIVITY_INDEX_CATALOG"})

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('background_image'),
    ]

    theme_panels = [
        FieldPanel('theme_background', widget=RadioSelectWithPicture),
        FieldPanel('theme_catalog', widget=RadioSelectWithPicture),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        activities = self.get_children().live().order_by('-first_published_at')
        context['activities'] = activities
        context['background_theme'] = self.theme_background.template_path
        context['catalog_theme'] = self.theme_catalog.template_path
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
# test markdown
# from wagtailmarkdown.edit_handlers import MarkdownPanel
# from wagtailmarkdown.fields import MarkdownField


# activity page for a single activity
class ActivityPage(Page):
    parent_page_types = ['ActivityIndexPage']
    subpage_types = []
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=500)
    date = models.DateField(("Publish Date"), default=datetime.date.today)
    application_form_link = models.CharField(max_length=500, null=True, blank=True)
    body = RichTextField(blank=True)
    cover_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    background_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                              related_name="activity_theme",
                              limit_choices_to={'type': "ACTIVITY"})
    activity_info = StreamField([
        ('activity_info', blocks.StructBlock([
            ('starting_time', blocks.DateTimeBlock(required=False, format='%Y-%m-%d %H:%M')),
            ('ending_time', blocks.DateTimeBlock(required=False, format='%Y-%m-%d %H:%M')),
            ('venue', blocks.CharBlock(max_length=500, required=False)),
            ('label', blocks.CharBlock(max_length=200, required=False, default="")),
        ])), ], null=True, blank=True)

    timezone = models.CharField(max_length=10, choices=[
        ('Melbourne', 'Melbourne'),
        ('Beijing', 'Beijing'),
    ], default='mel', null=True, blank=False)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('intro'),
        FieldPanel('date'),
        FieldPanel('application_form_link'),
        StreamFieldPanel('activity_info'),
        FieldPanel('timezone'),

        FieldPanel('body'),
        ImageChooserPanel('cover_image'),
        ImageChooserPanel('background_image'),
    ]

    theme_panels = [
        FieldPanel('theme', widget=RadioSelectWithPicture),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['theme'] = self.theme.template_path
        favorite = False
        if request.user:
            for page in request.user.favorite_activities.all():
                if self.id == page.id:
                    favorite = True
                    break
        context['favorite'] = favorite
        return context


# @register_setting
# class SocialMediaSettings(BaseSetting):
#     facebook = models.URLField(
#         help_text='Your Facebook page URL', null=True)
#     instagram = models.CharField(
#         max_length=255, help_text='Your Instagram username, without the @')
#     twitter = models.URLField(
#         help_text='Your Facebook page URL', null=True)
#     facebook_tab_panels = [
#         FieldPanel('facebook'),
#     ]
#     instagram_tab_panels = [
#         FieldPanel('instagram'),
#     ]
#     twitter_tab_panels = [
#         FieldPanel('twitter'),
#     ]
#
#     edit_handler = TabbedInterface([
#         ObjectList(facebook_tab_panels, heading='First tab'),
#         ObjectList(instagram_tab_panels, heading='Second tab'),
#         ObjectList(twitter_tab_panels, heading='Third tab'),
#     ])


class FormField(AbstractFormField):
    page = ParentalKey('ContactUsPage', related_name='form_fields')
    field_type = models.CharField(verbose_name=_('field type'), max_length=16, choices=CONTACT_PAGE_FORM_FIELD_CHOICES)
    panels = [
        FieldPanel('label'),
        FieldPanel('help_text'),
        FieldPanel('required'),
        FieldPanel('field_type', classname="formbuilder-type"),
        # FieldPanel('choices', classname="formbuilder-choices"),
        FieldPanel('default_value', classname="formbuilder-default"),
    ]


class ContactUsPage(AbstractEmailForm):
    parent_page_types = ['home.HomePage', 'vcssa.SubUnionHomePage']
    subpage_types = []
    show_in_menus_default = True
    background_image = models.ForeignKey(
        'wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    intro = RichTextField(blank=True, default="Please contact us through our WeChat, or leave a message")
    thank_you_text = RichTextField(blank=True, default="Thank you for contacting us! We will get back to you soon.")
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)

    facebook = models.URLField(blank=True, null=True, help_text='Your Facebook page URL')
    instagram = models.URLField(blank=True, max_length=255, help_text='Your Instagram page URL', null=True)
    weibo = models.URLField(blank=True, null=True, help_text='Your Weibo page URL')
    weChat = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        help_text='Your WeChat QR Code')

    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                              related_name="contact_theme",
                              limit_choices_to={'type': "CONTACT"})

    content_panels = [
        FieldPanel('title'),
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('background_image'),
        FieldPanel('address'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('facebook'),
        FieldPanel('instagram'),
        FieldPanel('weibo'),
        ImageChooserPanel('weChat'),

        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel(
            [
                FieldPanel('to_address', help_text='Please enter an email to receive notifications'),
                FieldPanel('subject'),
            ],
            heading="Email Configuration",
        ),
    ]

    theme_panels = [
        FieldPanel('theme', widget=RadioSelectWithPicture),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, request.FILES, page=self, user=request.user)

            if form.is_valid():
                form_submission = self.process_form_submission(form)
                # messages.add_message(request, constants_messages.SUCCESS_STICKY, 'The mail was sent successfully!')
                print(strip_tags(self.thank_you_text))
                messages.success(request, strip_tags(self.thank_you_text))
                # return self.render_landing_page(request, form_submission, *args, **kwargs)
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )

    def send_mail(self, form):
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['theme'] = self.theme.template_path
        return context


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'NewsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class NewsTagIndexPage(Page):
    parent_page_types = ['home.HomePage', 'vcssa.SubUnionHomePage']
    subpage_types = []
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                              related_name="news_tag_index_theme",
                              limit_choices_to={'type': "NEWS_TAGS_INDEX"})

    content_panels = Page.content_panels

    theme_panels = [
        FieldPanel('theme', widget=RadioSelectWithPicture),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        newspages = NewsPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['newspages'] = newspages
        context['theme'] = self.theme.template_path
        return context


class NewsPage(Page):
    parent_page_types = ['vcssa.NewsIndexPage']
    subpage_types = []
    author = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    intro = models.CharField(max_length=255, null=True, blank=True)
    body = RichTextField()
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                              related_name="news_page_theme",
                              limit_choices_to={'type': "NEWS"})

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        ImageChooserPanel('cover_image'),
        FieldPanel('intro'),
        FieldPanel('tags'),
        FieldPanel('body')
    ]

    theme_panels = [
        FieldPanel('theme', widget=RadioSelectWithPicture),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['theme'] = self.theme.template_path
        return context


class NewsIndexPage(Page):
    parent_page_types = ['home.HomePage', 'vcssa.SubUnionHomePage']
    subpage_types = ['vcssa.NewsPage']
    show_in_menus_default = True
    intro = models.CharField(max_length=500, blank=True)
    background_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    theme_background = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                         related_name="news_index_background_theme",
                                         limit_choices_to={'type': "NEWS_INDEX_BACKGROUND"})
    theme_content = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                      related_name="news_index_content_theme",
                                      limit_choices_to={'type': "NEWS_INDEX_CONTENT"})

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('background_image'),
    ]

    theme_panels = [
        FieldPanel('theme_background', widget=RadioSelectWithPicture),
        FieldPanel('theme_content', widget=RadioSelectWithPicture),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme Setting'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        news = self.get_children().live().order_by('-first_published_at')
        context['news'] = news
        context['background_theme'] = self.theme_background.template_path
        context['content_theme'] = self.theme_content.template_path
        return context
