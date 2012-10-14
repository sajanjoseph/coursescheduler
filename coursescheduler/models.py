

# Create your models here.
from django.db import models

#from django.forms import ChoiceField
from django.contrib.auth.models import User
import datetime



class Course(models.Model):
    students = models.ManyToManyField(User,related_name='course_students')
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User,related_name='course_creator')
    def __unicode__(self):
        return self.title
    
    class Meta:
		verbose_name_plural="Courses"

status_values = (
                 ('PEND','PENDING'),
                 ('FINI','FINISHED'),
                 )

class Task(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=200)
    submission_date = models.DateTimeField(default=lambda:datetime.datetime.now()+datetime.timedelta(days=1))#making this django.utils.timezone.now() causes error even with USE_TZ=True
    author = models.ForeignKey(User)
    status = models.CharField(max_length = 4,choices=status_values ,default = 'PEND')
    expected_duration = models.IntegerField(default=60,help_text='in minutes')
    closed_date = models.DateTimeField(null=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural="Tasks"
        ordering = ['submission_date']

