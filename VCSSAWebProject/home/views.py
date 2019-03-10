import os
import re

from django.contrib import messages
from django.core.files import File
from django.shortcuts import redirect

from home.models import BASE_THEME_PATH, BASE_DIR, Theme, THEME_CHOICES
from vcssa.templatetags.global_tags import MEDIA_DIR


def auto_load_theme(request):
    """Load all pre-stored themes. Put the directory of html files in BASE_THEME_PATH,
    Note that the order of the directory must be of the same as THEME_CHOICES in home.models.
    The name of corresponding preview photo must be the same as html file,
    and store under 'media' app."""
    # request = context['request']
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
    # theme_index = request.site.hostname + "/admin/home/theme"
    # print(theme_index)
    return redirect('/admin/home/theme/')


def bulk_delete_theme(request):
    Theme.objects.all().delete()
    return redirect('/admin/home/theme/')
