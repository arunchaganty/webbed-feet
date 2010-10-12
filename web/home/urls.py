from django.conf.urls.defaults import *

urlpatterns = patterns('web.home.views',
    (r'^logout/$', 'logout'),
    (r'^login/$', 'login'),
    (r'^ping/$', 'ping'),
    (r'^help/$', 'help'),
    (r'', 'home'),
)
