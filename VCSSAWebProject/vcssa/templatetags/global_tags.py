from django import template
from django.template import Template
from wagtail.core.models import Page
from home.models import HomePage
from vcssa.models import SubUnionHomePage

HOME_PAGE_LEVEL = 1
SUBUNION_HOME_LEVEL = 2
VCSSA_MENU_TEMPLATE = '{% load menu_tags %}{% section_menu max_levels=3 use_specific=USE_SPECIFIC_TOP_LEVEL template="menus/custom_main_menu.html" %}'
SUBUNION_MENU_TEMPLATE = '{% load menu_tags global_tags %}{% subunion_home as rootpage%}{% children_menu parent_page=rootpage max_levels=2 use_specific=USE_SPECIFIC_TOP_LEVEL template="menus/custom_main_menu.html" %}'


register = template.Library()


@register.simple_tag()
def vcssa_home():
    """ return vcssa home page to create menu """
    vcssa_home = HomePage.objects.filter(live=True)[HOME_PAGE_LEVEL]
    print(vcssa_home)
    return vcssa_home


@register.simple_tag(takes_context=True)
def subunion_home(context):
    """ return subunion home page to create menu """
    page = context['page']
    subunion_home = page.get_ancestors()[SUBUNION_HOME_LEVEL]
    print(subunion_home)
    return subunion_home


@register.simple_tag(takes_context=True)
def load_menu(context):
    """ load menu according to the level of the page """
    child_of_subunion = is_child_of_subunion(context)
    if child_of_subunion:
        return Template(SUBUNION_MENU_TEMPLATE).render(context)
    return Template(VCSSA_MENU_TEMPLATE).render(context)


@register.simple_tag(takes_context=True)
def is_child_of_subunion(context):
    request_page = context['page']
    child_of_subunion = False
    for page in SubUnionHomePage.objects.all():
        child_of_subunion = request_page.is_descendant_of(page) or child_of_subunion
    return child_of_subunion
