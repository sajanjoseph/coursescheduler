# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.http import HttpResponse
from coursescheduler.models import Course,Task
from coursescheduler.forms import CourseTitleForm,CourseForm,EditCourseForm,CourseChoicesForm
from coursescheduler.forms import TaskForm,TaskStatusForm,CompletionIntervalForm
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
import datetime
import simplejson;
from django.core.urlresolvers import reverse
from django.core.cache import cache
from models import PENDING,FINISHED

prefix = 'tasks'
def key_function(args,prefix=prefix):
    #sample tasks-myusername-2012-01-22'
    #
    keyargs =[prefix]
    keyargs.extend(args)
    key = '-'.join(keyargs)
    return key
    

def logout(request):
    return logout_then_login(request)


def custom_render(request,context,template):
    req_context=RequestContext(request,context)
    return render_to_response(template,req_context)

@login_required
def home(request,template_name,page_title):
    pend_tasks_data = []
    pend_tasks = get_pending_tasks(request.user)
    pend_tasks_dump = ''
    for task in pend_tasks:
        id = task.id;
        name = task.name
        sub_date = task.submission_date
        link = reverse('task_details',args=[id])
        pend_tasks_data.append(
                          {
                           'title':name,
                           'start':sub_date.strftime("%Y-%m-%d"),
                           'end':sub_date.strftime("%Y-%m-%d"),
                           'url': link
                           }
                          )
        pend_tasks_dump = simplejson.dumps(pend_tasks_data)
    return custom_render(request,{'page_title':page_title,'pend_tasks_dump':pend_tasks_dump},template_name)

def get_form_data(request):
    return request.POST if request.method == 'POST' else None


#def duplicate_course(user,title):
#    if Course.objects.filter(title=title).count()==0:
#        return False
#    else:
#        return True

def get_course_from_title(user,course_title):
    courses = Course.objects.filter(creator=user,title__iexact=course_title)
    if courses:
        course = courses[0]
    else:
        course = Course(title=course_title,description=course_title)
        course.creator = user
        course.save()
#    if user not in course.students.all():
#        course.students.add(user)
#        course.save()
    return course

@login_required
@transaction.commit_on_success
def create_task(request,template_name,page_title):
    form_data = get_form_data(request)
    task_form = TaskForm(form_data)
    #user_courses = Course.objects.filter(creator=request.user)
    course_title_form = CourseTitleForm(form_data)
    course_choices_form = CourseChoicesForm(request.user,form_data)
    context = {'page_title':page_title,'task_form':task_form,'course_title_form':course_title_form,'course_choices_form':course_choices_form}
    allformsvalid = validate_forms([task_form,course_title_form,course_choices_form])
    if request.method == 'POST' and allformsvalid:
        #TODO redirect to task detail
        course_title = course_title_form.cleaned_data['title']
        course_title = course_title.strip()
        if len(course_title)>0:
            course = get_course_from_title(request.user,course_title)
        else:
            course = course_choices_form.cleaned_data['courseoption']
            if not course:
                from django.forms.util import ErrorList
                course_choices_form._errors['courseoption']= ErrorList([u"Select a course"])
                return custom_render(request,context,template_name)
            #course = Course.objects.get(id=course_choice_id)
            if course and request.user not in course.students.all():
                course.students.add(request.user)
                #print 'added user to course'
                course.save()
        task = task_form.save(commit=False)
        task.author = request.user
        task.course = course
        task.save()
        #cache clear for pending tasks
        pending_tasks_key = key_function([request.user.username],'pending-tasks')
        if cache.has_key(pending_tasks_key):
            cache.delete(pending_tasks_key)
        return redirect('pending_tasks')
    return custom_render(request,context,template_name)

def validate_forms(forms):
    for entry in forms:
        if not entry.is_valid():
            return False
    return True

def clear_tasks_from_cache(task,user):
    if task.status==PENDING:
        pending_tasks_key = key_function([user.username],'pending-tasks')
        if cache.has_key(pending_tasks_key):
            cache.delete(pending_tasks_key)
    else:
        finished_tasks_key = key_function([user.username],'finished-tasks')
        if cache.has_key(finished_tasks_key):
            cache.delete(finished_tasks_key)

@login_required
@transaction.commit_on_success
def edit_task(request,id,template_name,page_title):
    form_data = get_form_data(request)
    task = get_object_or_404(Task,pk=id,author=request.user)
    clear_tasks_from_cache(task,request.user)
    oldcourse = task.course#added
    task_form = TaskForm(form_data,instance=task)
    task_status_form = TaskStatusForm(form_data)
    course_title_form = CourseTitleForm(form_data)
    course_choices_form = CourseChoicesForm(request.user,form_data)
    allformsvalid = validate_forms([task_form,task_status_form,course_title_form,course_choices_form])
    context = {'page_title':page_title,'task_form':task_form,'task_status_form':task_status_form}
    context.update({'course_title_form':course_title_form,'course_choices_form':course_choices_form})
    if request.method == 'POST' and allformsvalid:
        #if valid entry in course text field get/create course
        #else get course from dropdown list
        course_title = course_title_form.cleaned_data['title']
        #course_from_title(course_title)
        course_title = course_title.strip()
        if len(course_title)>0:
            course = get_course_from_title(request.user,course_title)
        else:
            #ModelChoiceForm returns a course instance
            course = course_choices_form.cleaned_data['courseoption']
            if request.user not in course.students.all():
                course.students.add(request.user)
                course.save()
        # get name,submission_date from form and update task
        task_name = task_form.cleaned_data['name']
        submission_date = task_form.cleaned_data['submission_date']
        task_status = task_status_form.cleaned_data['statusoption']
        if task.status==PENDING and task_status==FINISHED:
            task.closed_date = datetime.datetime.now()
        task.name = task_name
        task.submission_date = submission_date
        task.status = task_status
        #if newcourse diff from oldcourse,then check if user has other tasks for the oldcourse,else remove user from students
        if course!=oldcourse:
            #print 'different course set for task:',task
            usertasks_for_oldcourse = oldcourse.task_set.filter(author=request.user)
            if usertasks_for_oldcourse.count()==1:
                oldcourse.students.remove(request.user)
        task.course = course
        task.save()
        clear_tasks_from_cache(task,request.user)
        #cache clear  IS THIS WORKING???
        
        remove_if_has_no_tasks(oldcourse)#delete course with no tasks at all
        return redirect('pending_tasks')
    
    #if GET set initial value of course in dropdown list
    course_choices_form = CourseChoicesForm(request.user,initial={'courseoption':task.course.id})
    task_status_form = TaskStatusForm(initial={'statusoption':task.status})
    context.update({'course_choices_form':course_choices_form,'task_status_form':task_status_form})
    return custom_render(request,context,template_name)

"""
if this course has no tasks ,delete the course
"""
def remove_if_has_no_tasks(course):
    taskscount=course.task_set.count()
    if taskscount==0:
        course.delete()

@login_required
@transaction.commit_on_success
def delete_task(request,id):
    task = get_object_or_404(Task,id=id,author=request.user)
    clear_tasks_from_cache(task,request.user)
    course = task.course
    task.delete()
    num_my_other_tasks_for_this_course = Task.objects.filter(author=request.user,course=course).count()
    #print 'num_my_other_tasks_for_this_course=',num_my_other_tasks_for_this_course
    if num_my_other_tasks_for_this_course==0:
        course.students.remove(request.user)
        #print 'removed %s from course.students'%request.user.username
    numstudents = course.students.count()
    #print 'numstudents=',numstudents
    if numstudents==0:
        course.delete()
    return redirect('pending_tasks')

@login_required
def task_details(request,id,template_name,page_title):
    task = get_object_or_404(Task,id=id,author=request.user)
    context ={'page_title':page_title,'task':task}
    return custom_render(request,context,template_name)

@login_required
def tasks(request,template_name,page_title):
    pend_tasks = get_pending_tasks(request.user)
    fini_tasks = get_finished_tasks(request.user)
    total = len(pend_tasks)+len(fini_tasks)
    context = {'page_title':page_title,'pending_tasks':pend_tasks,'finished_tasks':fini_tasks,'total':total}
    return custom_render(request,context,template_name)

def get_pending_tasks(user):
    key = key_function([user.username],'pending-tasks')
    pending_tasks = cache.get(key) if cache.has_key(key) else None
    if not pending_tasks:
        pending_tasks = Task.objects.filter(author=user,status=PENDING)
        #print 'DBQUERY:pending tasks got from db'
        cache.set(key,pending_tasks)
    return pending_tasks


def get_finished_tasks(user):
    key = key_function([user.username],'finished-tasks')
    finished_tasks = cache.get(key) if cache.has_key(key) else None
    if not finished_tasks:
        finished_tasks = Task.objects.filter(author=user,status=FINISHED).order_by('-closed_date')
        #print 'DBQUERY:finished tasks got from db'
        cache.set(key,finished_tasks)
    return finished_tasks
    
@login_required
def pending_tasks(request,template_name,page_title):
    form_data = get_form_data(request)
    pending_tasks = get_pending_tasks(request.user)
    current_date = datetime.datetime.now()
    context={'page_title':page_title,'pending_tasks':pending_tasks,'current_date':current_date}
    return custom_render(request,context,template_name)

@login_required
def closed_tasks(request,template_name,page_title):
    form_data = get_form_data(request)
    closed_tasks = get_finished_tasks(request.user)
    completionIntervalForm = CompletionIntervalForm()
    #print completionIntervalForm
    context={'page_title':page_title,'closed_tasks':closed_tasks,'completionIntervalForm':completionIntervalForm}
    return custom_render(request,context,template_name)

@login_required
def closed_tasks_of_interval(request,template_name,page_title):
    form_data = get_form_data(request)
    completionIntervalForm = CompletionIntervalForm(form_data)
    days = 1
    if request.method=='POST' and completionIntervalForm.is_valid():
        days = completionIntervalForm.cleaned_data['intervaloption']
    print 'days=',days
    days = int(days)
    closed_tasks = get_finished_tasks_of_interval(request.user,days)
    
    #print completionIntervalForm
    context={'page_title':page_title,'closed_tasks':closed_tasks,'completionIntervalForm':completionIntervalForm}
    return custom_render(request,context,template_name)

def get_finished_tasks_of_interval(user,days):
    #key = key_function([user.username],'finished-tasks-gap')
    #finished_tasks = cache.get(key) if cache.has_key(key) else None
    #get all tasks that have a finished status and a diff btw creation_date and closed_date >= days
    
#    if not finished_tasks:
#        finished_tasks = Task.objects.filter(author=user,status=FINISHED,closed_date__gt=F('creation_date') + datetime.timedelta(days=days)).order_by('-closed_date')
#        #print 'DBQUERY:finished tasks got from db'
#        print 'finished_tasks=',finished_tasks
#        cache.set(key,finished_tasks)
    finished_tasks = Task.objects.filter(author=user,status=FINISHED,closed_date__gt=F('creation_date') + datetime.timedelta(days=days)).order_by('-closed_date')
    print 'get_finished_tasks_of_interval=',finished_tasks
    return finished_tasks

def duration_in_days(creation_date,closed_datetime):
    closed_date = datetime.date(closed_datetime.year,closed_datetime.month,closed_datetime.day)
    return (closed_date - creation_date).days

@login_required
def create_course(request,template_name,page_title):
    form_data = get_form_data(request)
    course_form = CourseForm(form_data)
    context = {'page_title':page_title,'course_form':course_form}
    valid_form = course_form.is_valid()
    if request.method == 'POST' and valid_form:
        course = course_form.save(commit=False)
        course.creator = request.user
        course.save()
        #add user to students only when a task is created for that course
        #course.students.add(request.user)
        #course.save()
        return redirect('courses')
    return custom_render(request,context,template_name)

@login_required
@transaction.commit_on_success
def edit_course(request,id,template_name,page_title):
    course=get_object_or_404(Course,pk=id,creator=request.user)
    form_data = get_form_data(request)
    edit_course_form = EditCourseForm(form_data,instance=course)
    context = {'page_title':page_title,'edit_course_form':edit_course_form}
    valid_form = edit_course_form.is_valid()
    if request.method =='POST' and valid_form:
        desc = edit_course_form.cleaned_data['description']
        course.description = desc
        course.save()
        return redirect('courses')
    return custom_render(request,context,template_name)
    
@login_required
def courses(request,template_name,page_title):
    from django.db.models import Q
    #all courses where user is a student or a creator
    courses = Course.objects.filter(Q(students=request.user)|Q(creator=request.user))
    #courses = Course.objects.filter(students = request.user ).order_by('title')
    context = {'page_title':page_title,'courses':courses}
    return custom_render(request,context,template_name)

@login_required
@transaction.commit_on_success 
def delete_course(request,id):
    #get all tasks of user that are of this course
    course = get_object_or_404(Course,pk=id,creator=request.user)
    tasks = Task.objects.filter(author=request.user,course=course)
    #delete those tasks
    for task in tasks:
        task.delete()
    #remove user from course's students
    #course.students.remove(request.user)
    #if course.students empty, delete course
    #print 'course.students.count()=',course.students.count()
    if course.students.count() == 0:
        course.delete()
        #print 'deleted course'
    return redirect('courses')


       