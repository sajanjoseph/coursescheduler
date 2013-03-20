from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coursehelper.views.home', name='home'),
    url(r'', include('coursescheduler.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)

#urlpatterns = patterns('',
#    # Examples:
#    # url(r'^$', 'coursehelper.views.home', name='home'),
#    url(r'^coursescheduler/', include('coursescheduler.urls')),
#
#    # Uncomment the admin/doc line below to enable admin documentation:
#    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),
#    url(r'^coursehelper_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
#    
#)