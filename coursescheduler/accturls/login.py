'''
Created on Sep 19, 2012

@author: sajan
'''
from registration.forms import RegistrationFormUniqueEmail
from registration.views import register
from registration.urls  import urlpatterns as regpatterns
from django.conf.urls.defaults import *

urlpatterns=patterns('',
url(r'^login/$','django.contrib.auth.views.login',{'template_name':'scheduler/mylogin.html'},name='coursescheduler_login'),
url(r'^logout/$', 'coursescheduler.views.logout', {}, name = 'coursescheduler_logout'),
)
custom_reg_patterns=patterns('',
     url(r'^register/', register, 
      {'form_class':RegistrationFormUniqueEmail ,'backend':'registration.backends.default.DefaultBackend'},
      
      name='registration_register'),
)
urlpatterns+=custom_reg_patterns


urlpatterns += regpatterns