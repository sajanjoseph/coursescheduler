'''
Created on Sep 13, 2012

@author: sajan
'''
from coursescheduler.models import Course,Task
from django.contrib import admin

admin.site.register(Course)
admin.site.register(Task)