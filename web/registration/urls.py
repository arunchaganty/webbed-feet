from django.conf.urls.defaults import *

urlpatterns = patterns('web.home.views',
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^register/$', 'register'),
    (r'^forgot/$', 'forgot_password'),
    (r'^change/$', 'change_password'),
)
