import os
import re

from django import template
from django.contrib import messages
from django.core.files import File
from django.template import Template
from home.models import HomePage,Theme,THEME_CHOICES
from vcssa.models import SubUnionHomePage

HOME_PAGE_LEVEL = 1
SUBUNION_HOME_LEVEL = 2
VCSSA_MENU_TEMPLATE = '{% load menu_tags %}{% section_menu max_levels=3 use_specific=USE_SPECIFIC_TOP_LEVEL template="menus/custom_main_menu.html" %}'
SUBUNION_MENU_TEMPLATE = '{% load menu_tags global_tags %}{% subunion_home as rootpage%}{% children_menu parent_page=rootpage max_levels=2 use_specific=USE_SPECIFIC_TOP_LEVEL template="menus/custom_main_menu.html" %}'

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
MEDIA_DIR = 'media\\previews\\'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media\\previews\\')

BASE_THEME_PATH = ['\\home\\templates\\home\\includes\\backgrounds\\',
                   '\\home\\templates\\home\\includes\\slides\\',
                   '\\home\\templates\\home\\includes\\news\\',
                   '\\vcssa\\templates\\vcssa\\includes\\about\\',
                   '\\vcssa\\templates\\vcssa\\includes\\activity_index\\background\\',
                   '\\vcssa\\templates\\vcssa\\includes\\activity_index\\catalog\\',
                   '\\vcssa\\templates\\vcssa\\includes\\activity\\',
                   '\\vcssa\\templates\\vcssa\\includes\\contact_us\\',
                   '\\vcssa\\templates\\vcssa\\includes\\news_tag_index\\',
                   '\\vcssa\\templates\\vcssa\\includes\\news\\',
                   '\\vcssa\\templates\\vcssa\\includes\\news_index\\background\\',
                   '\\vcssa\\templates\\vcssa\\includes\\news_index\\content\\',
                   ]

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
            for file_name in file_names:
                if re.search("(\.html)$", file_name):  # find all html files
                    html_path = BASE_DIR + theme_path + file_name
                    name, tail = file_name.split(".")  # use html file name as template name
                    preview_file_name = name + '.jpg'  # preview .jpg name must be the same as html file
                    preview_path = MEDIA_DIR + preview_file_name
                    if not Theme.objects.filter(template_path=html_path).exists():  # if the theme is not added
                        new_theme = Theme.objects.create(name=name, template_path=html_path, type=THEME_CHOICES[count][0])
                        if os.path.exists(preview_path):
                            try:  # store preview photo in db
                                with open(preview_path, "rb") as f:
                                    # with open("media\\previews\\"+preview_file_name, "rb") as f:
                                    new_theme.preview_photo = File(f)
                                    new_theme.save()
                            except IOError:
                                messages.error(request, "Cannot Load File" + preview_path)
                        else:
                            messages.error(request, "File " + preview_path + " does not exist.")
        count += 1
