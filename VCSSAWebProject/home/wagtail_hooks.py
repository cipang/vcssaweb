import os
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from wagtail.contrib.modeladmin.views import CreateView
from wagtail.sites.views import IndexView
from wagtail.admin.utils import permission_required
from wagtail.core.compat import AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME
from home.models import Theme

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
# add_user_perm = "{0}.add_{1}".format(AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower())


# class ThemeCreateView(CreateView):
#     # @permission_required(add_user_perm)
#     def auto_load_themes(self, request):
#         print("in")
#         if request.method == "GET":
#             print("project dir:")
#             print(PROJECT_DIR)
#             print("base dir:")
#             print(BASE_DIR)
#             cpt = sum([len(files) for r, d, files in os.walk(PROJECT_DIR)])
#             print(cpt)


class ThemeModelAdmin(ModelAdmin):
    model = Theme
    menu_label = 'Theme'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    # index_view_class = ThemeIndexView
    list_display = ('name', 'type', 'template_path')
# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(ThemeModelAdmin)
