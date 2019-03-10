from django.conf.urls import url
from members import views

app_name = 'members'
urlpatterns = [
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^resend/$', views.resend, name='resend'),
    url(r'^account-home/$', views.accounthome, name='account_home'),
    url(r'^edit-profile/$', views.edit_profile, name='edit_profile'),
    url(r'^send-email/$', views.send_validation_email, name='send_email'),
]


