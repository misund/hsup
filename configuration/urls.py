from django.conf.urls import patterns, include, url
from django.contrib import admin
from llop.models import *

import llop.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^llop/', include(llop.urls)),
    url(r'^add_feed/$', 'llop.views.add_feed', name='add_feed'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
