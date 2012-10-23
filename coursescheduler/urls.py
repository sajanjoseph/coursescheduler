'''
Created on Sep 13, 2012

@author: sajan
'''
from django.conf.urls.defaults import *

urlpatterns=patterns('',
  url(r'^account/',include('coursescheduler.accturls.login')),
  url(r'^$','coursescheduler.views.home',
      {
         'template_name':'scheduler/home.html',
         'page_title':'Home'
       },
      name='home'),
  url(r'^create_course/$','coursescheduler.views.create_course',
      {
         'template_name':'scheduler/create_course.html',
         'page_title':'Create New Course'
       },
      name='create_course'),
                     
  url(r'^edit_course/(?P<id>\d+)/$','coursescheduler.views.edit_course',
      {
         'template_name':'scheduler/edit_course.html',
         'page_title':'Edit Course'
       },
      name='edit_course'),
                     
  url(r'^courses/$','coursescheduler.views.courses',
      {
         'template_name':'scheduler/courses.html',
         'page_title':'Courses'
       },
      name='courses'),
                     
  url(r'^delete_course/(?P<id>\d+)/$','coursescheduler.views.delete_course',
      
      name='delete_course'),
                     
  url(r'^create_task/$','coursescheduler.views.create_task',
      
      {
        'template_name' : 'scheduler/create_task.html',
        'page_title':'Create Task'
       },
      name='create_task'),
                     
  url(r'^edit_task/(?P<id>\d+)/$','coursescheduler.views.edit_task',
      {
       'template_name':'scheduler/edit_task.html',
        'page_title':'Edit Task'
       },
      
      name='edit_task'),

  url(r'^delete_task/(?P<id>\d+)/$','coursescheduler.views.delete_task',
      name='delete_task'),

  url(r'^task_details/(?P<id>\d+)/$','coursescheduler.views.task_details',
      {
        'template_name':'scheduler/task_details.html',
        'page_title':'Task Details'
       },
      name='task_details'),                   
                     
#  url(r'^tasks/$','coursescheduler.views.tasks',
#      {
#         'template_name':'scheduler/tasks.html',
#         'page_title':'Tasks'
#       },
#      name='tasks'),
                     
  url(r'^pending_tasks/$','coursescheduler.views.pending_tasks',
      {
         'template_name':'scheduler/pending_tasks.html',
         'page_title':'Pending Tasks'
       },
      name='pending_tasks'),
                     
   url(r'^closed_tasks/$','coursescheduler.views.closed_tasks',
      {
         'template_name':'scheduler/closed_tasks.html',
         'page_title':'Closed Tasks'
       },
      name='closed_tasks'),
                    
)