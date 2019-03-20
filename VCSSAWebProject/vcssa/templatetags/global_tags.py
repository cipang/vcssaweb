import os
import re

from django import template
from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.template import Template
from wagtail.core.models import Collection, CollectionViewRestriction

from home.models import HomePage,Theme,THEME_CHOICES, BASE_THEME_PATH, BASE_DIR
from users.models import Subunions
from vcssa.models import SubUnionHomePage, ContactUsPage

HOME_PAGE_LEVEL = 0
SUBUNION_HOME_LEVEL = 2
VCSSA_MENU_TEMPLATE = '{% load menu_tags %}{% section_menu max_levels=3 use_specific=2 template="menus/custom_main_menu.html" %}'
SUBUNION_MENU_TEMPLATE = '{% load menu_tags global_tags %}{% subunion_home as rootpage%}{% children_menu parent_page=rootpage max_levels=2 use_specific=USE_SPECIFIC_TOP_LEVEL template="menus/custom_main_menu.html" %}'
NONE_PAGE_MENU_TEMPLATE = '{% include "menus/custom_main_menu.html" %}'


MEDIA_DIR = 'media/previews/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/previews/')

ADMIN_PERMISSIONS = ['access_admin', 'add_user', 'change_user', 'delete_user', 'view_user']
EDITOR_PERMISSIONS = ['access_admin']

register = template.Library()


@register.simple_tag(takes_context=True)
def current_user(context):
    try:
        request = context['request']
        name = request.user.first_name
    except:
        try:
            name = context['profile']['First Name']
        except:
            name = None
    return name


@register.simple_tag()
def vcssa_home():
    """ return vcssa home page to create menu """
    vcssa_home = HomePage.objects.filter(live=True)[HOME_PAGE_LEVEL]
    return vcssa_home


@register.simple_tag(takes_context=True)
def subunion_home(context):
    """ return subunion home page to create menu """
    page = context['page']
    if page in SubUnionHomePage.objects.all():
        return page
    subunion_home = None
    try:
        subunion_home = page.get_ancestors()[SUBUNION_HOME_LEVEL]
    except:
        print("Error on loading subunion home menu")
    return subunion_home


@register.simple_tag(takes_context=True)
def contact_us_page(context):
    if is_child_of_subunion(context):
        home = subunion_home(context)
        for child in home.get_children().specific():
            if child in ContactUsPage.objects.all():
                return child
    else:
        for child in vcssa_home().get_children().specific():
            if child in ContactUsPage.objects.all():
                return child
    return None


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
        if request_page in SubUnionHomePage.objects.all():
            return True
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
        # messages.success(home_background_path, request)
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
                        new_theme = Theme.objects.create(name=name, template_path=html_path, type=THEME_CHOICES[count][0])
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


@register.simple_tag(takes_context=True)
def add_subunion_groups(context):
    """Create new group according to Subunion objects"""
    request = context['request']
    for subunion in Subunions.objects.all():
        admin_group = None
        editor_group = None
        if not Group.objects.filter(name=subunion.name + " Member"):
            try:
                Group.objects.create(name=subunion.name + " Member")
            except:
                messages.error(request, "Cannot create member group for the new subunion.")

        if not Group.objects.filter(name=subunion.name + " Admin"):
            try:
                admin_group = Group.objects.create(name=subunion.name + " Admin")
            except:
                messages.error(request, "Cannot create admin group for the new subunion.")
        if not Group.objects.filter(name=subunion.name + " Editor"):
            try:
                editor_group = Group.objects.create(name=subunion.name + " Editor")
            except:
                messages.error(request, "Cannot create editor group for the new subunion.")
            try:
                union_admin_permission = Permission.objects.get(codename='union_admin')
            except ObjectDoesNotExist:
                content_type = ContentType.objects.get(id=3)
                union_admin_permission = Permission.objects.create(codename='union_admin',
                                                                   name='Administrator of Union',
                                                                   content_type=content_type)
            try:
                union_editor_permission = Permission.objects.get(codename='union_editor')
            except ObjectDoesNotExist:
                content_type = ContentType.objects.get(id=3)
                union_editor_permission = Permission.objects.create(codename='union_editor',
                                                                    name='Editor of Union',
                                                                    content_type=content_type)
            try:
                admin_group.permissions.add(union_admin_permission)
                editor_group.permissions.add(union_editor_permission)
                for admin_codename in ADMIN_PERMISSIONS:
                    admin_group.permissions.add(Permission.objects.get(codename=admin_codename))
                for editor_codename in EDITOR_PERMISSIONS:
                    editor_group.permissions.add(Permission.objects.get(codename=editor_codename))
            except:
                messages.error(request, "Error occurred when setting permissions to new subunion groups.")

        if not Collection.objects.filter(name=subunion.name):
            try:
                editor_group = Group.objects.filter(name=subunion.name + " Editor")
                admin_group = Group.objects.filter(name=subunion.name + " Admin")
                root_coll = Collection.get_first_root_node()
                collection = root_coll.add_child(name=subunion.name)
                restriction = CollectionViewRestriction.objects.create(collection=collection)
                restriction.restriction_type = 'groups'
                restriction.groups.add(editor_group.values_list('id', flat=True)[0])
                restriction.groups.add(admin_group.values_list('id', flat=True)[0])
            except:
                messages.error(request, "Cannot create collection for the new subunion.")
