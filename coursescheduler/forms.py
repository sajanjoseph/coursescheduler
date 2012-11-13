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
    courseoption = forms.ModelChoiceField(
                           queryset = Course.objects.none(),
                           required=False,label='Course')
    def __init__(self, coursecreator,*args, **kwargs):
        super(CourseChoicesForm, self).__init__(*args, **kwargs)
        self.creator=coursecreator
        #self.courseoption = forms.ModelChoiceField(queryset=Course.objects.filter(creator=self.creator),required=False,label='Course')
        self.fields['courseoption'].queryset = Course.objects.filter(creator=self.creator)
        print "self.fields['courseoption'].queryset:after=",self.fields['courseoption'].queryset
    
#class CourseChoicesForm(forms.Form):
#    courseoption = forms.ChoiceField(choices=[],required=False,label='Course')
#    def __init__(self, *args, **kwargs):
#        super(CourseChoicesForm, self).__init__(*args, **kwargs)
#        self.fields['courseoption'].choices = [(x.id,x.title) for x in Course.objects.all()]

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('author','course','status','closed_date')
    def clean_expected_duration(self):
        exp_dur = self.cleaned_data['expected_duration']
        if exp_dur <0:
            raise forms.ValidationError('Provide positive integer')
        return exp_dur
    def clean_completed_till_now(self):
        completed = self.cleaned_data['completed_till_now']
        if completed <0:
            raise forms.ValidationError('Provide positive integer')
        return completed


class TaskStatusForm(forms.Form):
    statusoption = forms.ChoiceField(choices =[],label='Status')
    def __init__(self,*args,**kwargs):
        super(TaskStatusForm,self).__init__(*args,**kwargs)
        self.fields['statusoption'].choices=[(x,y) for (x,y) in status_values]