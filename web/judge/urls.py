from django.conf.urls.defaults import *

urlpatterns = patterns('web.judge.views',
    (r'^manage/$', 'manage'),
    (r'^standings/$', 'standings'),
    # Result pages
    (r'^results/$', 'results'),
    (r'^results/all/$', 'results'),
    (r'^results/all/(?P<page>[0-9]+)/$', 'results'),
    (r'^results/bot/(?P<bot_id>[0-9]+)/$', 'results'),
    (r'^results/bot/(?P<bot_id>[0-9]+)/(?P<page>[0-9]+)/$', 'results'),
)
