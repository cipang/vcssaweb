from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import login
from django.views.defaults import page_not_found

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from users import views as userview
from vcssa import views as vcssaview
from home import views as homeview


handler404 = 'members.views.handler404'

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/images/chooser/$', vcssaview.chooser),
    url(r'^admin/users/add/$', userview.create),
    url(r'^admin/users/$', userview.index),
    url(r'^admin/users/(\d+)/$', userview.edit),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^messages/', include('messages_extends.urls')),

    url(r'^members/', include('members.urls', namespace='members')),
    url(r'^load_theme/$', homeview.auto_load_theme, name='load_theme'),
    url(r'^delete_theme/$', homeview.bulk_delete_theme, name='delete_theme'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)