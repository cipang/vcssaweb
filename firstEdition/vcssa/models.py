from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
import datetime

NUM_OF_SUBUNIONS = 8


class AboutPage(Page):
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
        InlinePanel('activity_index_images', label="Activity images"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        activities = self.get_children().live().order_by('-first_published_at')
        context['activities'] = activities
        return context


# activity index page images
class ActivityIndexPageGalleryImage(Orderable):
    page = ParentalKey(ActivityIndexPage, on_delete=models.CASCADE, related_name='activity_index_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
    ]


# activity page for a single activity
class ActivityPage(Page):
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=500)
    date = models.DateField(("Date"), default=datetime.date.today)
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
        ImageChooserPanel('background_image'),
    ]
