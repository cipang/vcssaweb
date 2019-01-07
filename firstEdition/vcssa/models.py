from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

NUM_OF_SUBUNIONS = 8


class Fields:
    pass


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
    content_panels = Page.content_panels + [FieldPanel('intro'), ]

    def get_context(self, request):
        context = super().get_context(request)
        subunion_names = []
        subunion_intros = []
        subunion_logos = []

        for i in range(NUM_OF_SUBUNIONS):
            subunion_names.append(getattr(self, 'subunion_' + str(i + 1) + '_name'))
            subunion_intros.append(getattr(self, 'subunion_' + str(i + 1) + '_intro'))
            subunion_logos.append(getattr(self, 'subunion_' + str(i + 1) + '_logo'))

        context['subunions'] = zip(subunion_names, subunion_intros, subunion_logos)
        return context


class SubUnionIndexPageGalleryImage(Orderable):
    page = ParentalKey(SubUnionIndexPage, on_delete=models.CASCADE, related_name='sub_union_images')
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
    ]


def add_field(sender, **subunion):
    namefield = models.CharField(subunion.get('attrname_name'), max_length=30, default=subunion.get('default_name'))
    namefield.contribute_to_class(sender, subunion.get('attrname_name'))
    introfield = models.CharField(subunion.get('attrname_intro'), max_length=200, default=subunion.get('default_intro'))
    introfield.contribute_to_class(sender, subunion.get('attrname_intro'))
    logofield = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL,
                                  related_name=subunion.get('related_name'))
    logofield.contribute_to_class(sender, subunion.get('attrname_logo'))


def add_parameters(self):
    default_name_list = ["Deakin University", "La Trobe University", "Monash University",
                         "RMIT University", "Swinburne University", "The University of Melbourne",
                         "University of Tasmania", "Victoria University"]
    default_intro = "Please add some intro to your union here"
    for i in range(NUM_OF_SUBUNIONS):
        subunion = {'attrname_name': "subunion_" + str(i + 1) + "_name",
                    'attrname_intro': "subunion_" + str(i + 1) + "_intro",
                    'attrname_logo': "subunion_" + str(i + 1) + "_logo",
                    'default_name': default_name_list[i],
                    'default_intro': default_intro,
                    'related_name': "subunion_" + str(i + 1) + "_logo"}
        add_field(SubUnionIndexPage, **subunion)
        SubUnionIndexPage.content_panels = SubUnionIndexPage.content_panels + [MultiFieldPanel([
            FieldPanel("subunion_" + str(i + 1) + "_name"),
            FieldPanel("subunion_" + str(i + 1) + "_intro"),
            ImageChooserPanel("subunion_" + str(i + 1) + "_logo"),
        ], heading="Sub Union " + str(i + 1) + " Info"), ]


add_parameters(SubUnionIndexPage)


class ActivityIndexPage(Page):
    intro = models.CharField(max_length=500, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('activity_index_images', label="Activity images"),
    ]


class ActivityIndexPageGalleryImage(Orderable):
    page = ParentalKey(ActivityIndexPage, on_delete=models.CASCADE, related_name='activity_index_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
    ]
