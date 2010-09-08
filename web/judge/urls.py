from django.conf.urls.defaults import *

urlpatterns = patterns('web.judge.views',
    (r'^manage/$', 'manage'),
    (r'^standings/$', 'standings'),
    (r'^results/$', 'results'),
    (r'^results/(?P<bot_id>[0-9]+)/$', 'results'),
)
