from django.conf.urls import patterns, include, url

from llop.views import *
from llop.models import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'llop.views.home', name='home'),
    url(r'^post/$', 'llop.views.post', name='post'),
    # url(r'^llop/', include('llop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
