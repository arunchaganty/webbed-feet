from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ( r'^home/', include('web.home.urls')),
    ( r'^accounts/', include('web.registration.urls')),
    ( r'^login/$', 'web.home.views.login'),
    ( r'^logout/$', 'web.home.views.logout'),

    (r'^judge/', include('web.judge.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'', 'web.home.views.home'),
)
