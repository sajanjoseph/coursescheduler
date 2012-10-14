'''
Created on Sep 19, 2012

@author: sajan
'''
from registration.urls  import urlpatterns as regpatterns
from django.conf.urls.defaults import *

urlpatterns=patterns('',
url(r'^login/$','django.contrib.auth.views.login',{'template_name':'scheduler/mylogin.html'},name='coursescheduler_login'),
url(r'^logout/$', 'coursescheduler.views.logout', {}, name = 'coursescheduler_logout'),
)
urlpatterns += regpatterns