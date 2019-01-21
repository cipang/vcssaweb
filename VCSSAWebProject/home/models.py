from django.db import models
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

HOME_PAGE_URL_PATH = '/home/homepage/'


class HomePage(Page):
    # parent_page_types = ['HomePage']
    welcome = models.CharField(max_length=200, default="Welcome to VCSSA!")
    background_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    logo_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    # related_news_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+',)
    index_pages = StreamField([
        ('index_page', blocks.PageChooserBlock(['vcssa.NewsPage', 'vcssa.ActivityPage'], null=True))
    ], null=True, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('welcome'),
        ImageChooserPanel('background_image'),
        ImageChooserPanel('logo_image'),
        StreamFieldPanel('index_pages'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context['menuitems'] = self.get_children().filter(live=True, show_in_menus=True)
        return context
