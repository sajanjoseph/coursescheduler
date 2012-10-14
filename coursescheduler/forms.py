'''
Created on Sep 22, 2012

@author: sajan
'''
from coursescheduler.models import Course,Task
from coursescheduler.models import status_values
from django import forms

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('students','creator',)
    def clean_title(self):
        title = self.cleaned_data['title']
        if Course.objects.filter(title=title).count()!=0:
            raise forms.ValidationError('course with same name exists')
        return title

class CourseTitleForm(forms.Form):
    title = forms.CharField(max_length=200,required=False)
    def clean(self):
        title = self.cleaned_data['title']
        print 'CourseTitleForm:clean:title=',title
        if not Course.objects.count() and not self.cleaned_data['title']:
            raise forms.ValidationError('you need to create a course')
        return self.cleaned_data


class EditCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['title'].widget.attrs['readonly'] = True
    class Meta:
        model = Course
        exclude = ('students','creator',)

class CourseChoicesForm(forms.Form):
    courseoption = forms.ModelChoiceField(queryset=Course.objects.all(),required=False,label='Course')
#class CourseChoicesForm(forms.Form):
#    courseoption = forms.ChoiceField(choices=[],required=False,label='Course')
#    def __init__(self, *args, **kwargs):
#        super(CourseChoicesForm, self).__init__(*args, **kwargs)
#        self.fields['courseoption'].choices = [(x.id,x.title) for x in Course.objects.all()]

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('author','course','status','closed_date')


class TaskStatusForm(forms.Form):
    statusoption = forms.ChoiceField(choices =[],label='Status')
    def __init__(self,*args,**kwargs):
        super(TaskStatusForm,self).__init__(*args,**kwargs)
        self.fields['statusoption'].choices=[(x,y) for (x,y) in status_values]