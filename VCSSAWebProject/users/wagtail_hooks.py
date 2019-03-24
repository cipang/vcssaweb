from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from users.models import Subunions

class SubunionModelAdmin(ModelAdmin):
    model = Subunions
    menu_label = 'Subunions'  # ditch this to use verbose_name_plural from model
    menu_icon = 'cog'  # change as required
    menu_order = 400  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    # index_view_class = ThemeIndexView
    list_display = ('name',)
# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(SubunionModelAdmin)