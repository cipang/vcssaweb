import os
import re

from django import template
from django.contrib import messages
from django.core.files import File
from django.template import Template
from home.models import HomePage, Theme, THEME_CHOICES, BASE_THEME_PATH, BASE_DIR
from vcssa.models import SubUnionHomePage

HOME_PAGE_LEVEL = 1
SUBUNION_HOME_LEVEL = 2
VCSSA_MENU_TEMPLATE = '{% load menu_tags %}{% section_menu max_levels=3 use_specific=2 template="menus/custom_main_menu.html" %}'
SUBUNION_MENU_TEMPLATE = '{% load menu_tags global_tags %}{% subunion_home as rootpage%}{% children_menu parent_page=rootpage max_levels=2 use_specific=USE_SPECIFIC_TOP_LEVEL template="menus/custom_main_menu.html" %}'
NONE_PAGE_MENU_TEMPLATE = '{% include "menus/custom_main_menu.html" %}'

MEDIA_DIR = 'media/previews/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/previews/')
# THEME_CHOICES = (
#     ("HOME_BACKGROUND", "Home Background"),
#     ("HOME_SLIDE", "Home Slide"),
#     ("HOME_NEWS", "Home News"),
#     ("ABOUT", "About"),
#     ("ACTIVITY_INDEX_BACKGROUND", "Activity Index Background"),
#     ("ACTIVITY_INDEX_CATALOG", "Activity Index Catalog"),
#     ("ACTIVITY", "Activity"),
#     ("CONTACT", "Contact Us"),
#     ("NEWS_TAGS_INDEX", "News Tag"),
#     ("NEWS", "News"),
#     ("NEWS_INDEX_BACKGROUND", "News Index Background"),
#     ("NEWS_INDEX_CONTENT", "News Index Content"),
#     ("SUBUNION_INDEX_BACKGROUND", "Subunion Index Background"),
#     ("SUBUNION_INDEX_CONTENT", "Subunion Index Content"),
# )
# BASE_THEME_PATH = ['\\home\\templates\\home\\includes\\backgrounds\\',
#                    '\\home\\templates\\home\\includes\\slides\\',
#                    '\\home\\templates\\home\\includes\\news\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\about\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\activity_index\\background\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\activity_index\\catalog\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\activity\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\contact_us\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\news_tag_index\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\news\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\news_index\\background\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\news_index\\content\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\subunion_index\\background\\',
#                    '\\vcssa\\templates\\vcssa\\includes\\subunion_index\\content\\',
#                    ]

register = template.Library()


@register.simple_tag()
def vcssa_home():
    """ return vcssa home page to create menu """
    vcssa_home = HomePage.objects.filter(live=True)[HOME_PAGE_LEVEL]
    return vcssa_home


@register.simple_tag(takes_context=True)
def subunion_home(context):
    """ return subunion home page to create menu """
    page = context['page']
    subunion_home = None
    try:
        subunion_home = page.get_ancestors()[SUBUNION_HOME_LEVEL]
    except:
        print("Error on loading subunion home menu")
    return subunion_home


@register.simple_tag(takes_context=True)
def logo_home_link(context):
    page = context['page']
    if is_child_of_subunion(context):
        link = page.get_ancestors()[SUBUNION_HOME_LEVEL]
    else:
        link = HomePage.objects.filter(live=True)[HOME_PAGE_LEVEL]
    return link


@register.simple_tag(takes_context=True)
def logo(context):
    """ return logo """
    page = context['page']
    if is_child_of_subunion(context):
        try:
            subhome = page.get_ancestors()[SUBUNION_HOME_LEVEL]
            subhome = SubUnionHomePage.objects.filter(title=subhome.title)
            for page in subhome:
                union_logo = page.logo
                return union_logo
        except:
            print("Error on loading vcssa logo")
    else:
        try:
            home = HomePage.objects.filter(live=True)[HOME_PAGE_LEVEL]
            return home.logo_image
        except:
            print("Error on loading vcssa logo")
    return None


@register.simple_tag(takes_context=True)
def load_menu(context):
    """ load menu according to the level of the page """
    if 'page' in context:
        child_of_subunion = is_child_of_subunion(context)
        if child_of_subunion:
            return Template(SUBUNION_MENU_TEMPLATE).render(context)
        return Template(VCSSA_MENU_TEMPLATE).render(context)
    else:
        home = vcssa_home()
        menu_items = home.get_children().filter(live=True, show_in_menus=True)
        context['menu_items'] = menu_items
        return Template(NONE_PAGE_MENU_TEMPLATE).render(context)


@register.simple_tag(takes_context=True)
def is_child_of_subunion(context):
    child_of_subunion = False
    try:
        request_page = context['page']
        for page in SubUnionHomePage.objects.all():
            child_of_subunion = request_page.is_descendant_of(page) or child_of_subunion
        return child_of_subunion
    except:
        return child_of_subunion


@register.simple_tag(takes_context=True)
def auto_load_theme(context):
    """Load all pre-stored themes. Put the directory of html files in BASE_THEME_PATH,
    Note that the order of the directory must be of the same as THEME_CHOICES in home.models.
    The name of corresponding preview photo must be the same as html file,
    and store under 'media' app."""
    request = context['request']
    count = 0  # auto increment type
    for theme_path in BASE_THEME_PATH:
        home_background_path = BASE_DIR + theme_path
        file_names = os.listdir(home_background_path)
        if file_names:  # if the directory has files
            file_names.sort()
            for file_name in file_names:
                if re.search("(\.html)$", file_name):  # find all html files
                    html_path = BASE_DIR + theme_path + file_name
                    name, tail = file_name.split(".")  # use html file name as template name
                    preview_file_name = name + '.jpg'  # preview .jpg name must be the same as html file
                    preview_path = MEDIA_DIR + preview_file_name
                    if not Theme.objects.filter(template_path=html_path).exists():  # if the theme is not added
                        new_theme = Theme.objects.create(name=name, template_path=html_path,
                                                         type=THEME_CHOICES[count][0])
                        if os.path.exists(preview_path):
                            try:  # store preview photo in db
                                with open(preview_path, "rb") as f:
                                    new_theme.preview_photo = File(f)
                                    new_theme.save()
                            except IOError:
                                messages.error(request, "Cannot Load File" + preview_path)
                        else:
                            messages.error(request, "File " + preview_path + " does not exist.")
        count += 1
