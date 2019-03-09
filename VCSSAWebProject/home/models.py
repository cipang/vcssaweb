import os

from django import forms
from django.db import models
from django.forms.widgets import ChoiceWidget
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable, PageBase
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

HOME_PAGE_URL_PATH = '/home/homepage/'
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR) + "/VCSSAWebProject"
# BASE_DIR = os.path.dirname(PROJECT_DIR)"
# todo change the BASE_DIR

THEME_CHOICES = (
    ("HOME_BACKGROUND", "Home Background"),
    ("HOME_SLIDE", "Home Slide"),
    ("HOME_NEWS", "Home News"),
    ("ABOUT", "About"),
    ("ACTIVITY_INDEX_BACKGROUND", "Activity Index Background"),
    ("ACTIVITY_INDEX_CATALOG", "Activity Index Catalog"),
    ("ACTIVITY", "Activity"),
    ("CONTACT", "Contact Us"),
    ("NEWS_TAGS_INDEX", "News Tag"),
    ("NEWS", "News"),
    ("NEWS_INDEX_BACKGROUND", "News Index Background"),
    ("NEWS_INDEX_CONTENT", "News Index Content"),
    ("SUBUNION_INDEX_BACKGROUND", "Subunion Index Background"),
    ("SUBUNION_INDEX_CONTENT", "Subunion Index Content"),
)

BASE_THEME_PATH = ['/home/templates/home/includes/backgrounds/',
                   '/home/templates/home/includes/slides/',
                   '/home/templates/home/includes/news/',
                   '/vcssa/templates/vcssa/includes/about/',
                   '/vcssa/templates/vcssa/includes/activity_index/background/',
                   '/vcssa/templates/vcssa/includes/activity_index/catalog/',
                   '/vcssa/templates/vcssa/includes/activity/',
                   '/vcssa/templates/vcssa/includes/contact_us/',
                   '/vcssa/templates/vcssa/includes/news_tag_index/',
                   '/vcssa/templates/vcssa/includes/news/',
                   '/vcssa/templates/vcssa/includes/news_index/background/',
                   '/vcssa/templates/vcssa/includes/news_index/content/',
                   '/vcssa/templates/vcssa/includes/subunion_index/background/',
                   '/vcssa/templates/vcssa/includes/subunion_index/content/',
                   ]


class RadioSelectWithPicture(ChoiceWidget):
    input_type = 'radio'
    template_name = 'home/radio_select_with_picture_widget.html'
    option_template_name = 'django/forms/widgets/radio_option.html'

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        select_image = None
        theme_object = Theme.objects.filter(name=label)
        for object in theme_object:
            select_image = object.preview_photo
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
            'wrap_label': True,
            'image': select_image
        }


class ThemeManager(models.Manager):
    def add_theme(self, name, preview_photo):
        theme = self.create(name=name, preview_photo=preview_photo)
        return theme


class Theme(models.Model):
    name = models.CharField(max_length=255, null=False, default="theme")
    type = models.CharField(max_length=255, choices=THEME_CHOICES, default="HOME_BACKGROUND")
    template_path = models.CharField(max_length=255, default=BASE_DIR, help_text="Enter full template path with name.")
    preview_photo = models.ImageField(null=True)
    objects = ThemeManager()
    panels = [
        FieldPanel('name'),
        FieldPanel('type', widget=forms.RadioSelect),
        FieldPanel('preview_photo'),
        FieldPanel('template_path')
    ]

    def __str__(self):
        if self.name is not None:
            return self.name


class HomePage(Page):
    # parent_page_types = ['HomePage']
    welcome = models.CharField(max_length=200, default="Welcome to VCSSA!")
    intro = models.CharField(max_length=255, default="The introduction of your union",
                             help_text="Introduce your union here")
    background_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    logo_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    posters = StreamField([('posters', ImageChooserBlock())], null=True, blank=True)
    index_pages = StreamField([
        ('index_page', blocks.PageChooserBlock(['vcssa.NewsPage', 'vcssa.ActivityPage'], null=True, required=False))
    ], null=True, blank=True)

    theme_background = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                         related_name="background_theme",
                                         limit_choices_to={'type': "HOME_BACKGROUND"})
    theme_slide = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                    related_name="slide_theme",
                                    limit_choices_to={'type': "HOME_SLIDE"})
    theme_news = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=False,
                                   related_name="news_theme",
                                   limit_choices_to={'type': "HOME_NEWS"})

    content_panels = Page.content_panels + [
        FieldPanel('welcome'),
        FieldPanel('intro'),
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
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context['background_theme'] = self.theme_background.template_path
        context['slide_theme'] = self.theme_slide.template_path
        context['news_theme'] = self.theme_news.template_path
        return context
