# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('website.views',
    url(r'^$', 'index', name='website-index'),
    url(r'^home/$', 'index', name='website-home'),
)
