"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse

class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase,self).setUp()
        self.client.login(username='sajan',password='sajan')

class TestLoginRequired(TestCase):
    def test_login_needed_to_view_create_course_page(self):
        response=self.client.get(reverse('create_course'))
        self.assertEqual(302,response.status_code)
        self.assertRedirects(response,reverse('coursescheduler_login')+'?next=/coursescheduler/create_course/')

class CourseTest(BaseTestCase):
    def test_add_course_get_view(self):
        response=self.client.get(reverse('create_course'))
        self.assertEqual(200,response.status_code)
        self.assertTemplateUsed(response, "scheduler/create_course.html")
        
    
        
