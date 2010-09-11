from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^home/', include('web.home.urls')),
    (r'^judge/', include('web.judge.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'', 'web.home.views.home'),
)
