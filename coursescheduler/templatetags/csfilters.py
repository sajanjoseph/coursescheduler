'''
Created on Oct 14, 2012

@author: sajan
'''
from django import template
from django.conf import settings
import datetime
register = template.Library()

@register.filter
def mts_to_hours(minutes_value):
    "converts a duration in minutes to hours& minutes"
    duration_minutes = int(minutes_value)
    hrs = duration_minutes/60
    mts = duration_minutes%60
    if duration_minutes > 0:
        #return str(duration_minutes/60) + ' hours, ' + str(duration_minutes%60) + ' minutes'
        output = ''
        if hrs==1:
            output = '1 hour'
        elif hrs>1:
            output = str(hrs)+' hours'
        if hrs and mts:
            output = output+' ,'
        if mts>0:
            output = output + str(mts)+ ' minutes'
        return output
    else:
        return '0'


@register.filter
def repeat(count):
    return range(int(count))

@register.filter
def diff_days(datetimeval):
    current = datetime.datetime.now()
    diff = datetimeval-current
    days = diff.days
    return days

@register.filter    
def dayslist(datetimeval):
    current = datetime.datetime.now()
    if datetimeval>current:
        diff = datetimeval-current
        days = diff.days
        #print 'days=',days
        return range(days)
    else:
        return []

@register.filter    
def halfdayslist(datetimeval):
    current = datetime.datetime.now()
    if datetimeval>current:
        diff = datetimeval-current
        totalhours = diff.seconds/3600
        halfdays = totalhours/12
        #print 'halfdays=',halfdays
        return range(halfdays)
    else:
        return []

@register.filter    
def quarterdayslist(datetimeval):
    current = datetime.datetime.now()
    if datetimeval>current:
        diff = datetimeval-current
        totalhours = diff.seconds/3600
        balance_hours_after_half_day = totalhours % 12
        quarterdays = balance_hours_after_half_day / 6
        #print 'quarterdays=',quarterdays
        return range(quarterdays)
    else:
        return []

@register.filter    
def hourslist(datetimeval):
    current = datetime.datetime.now()
    if datetimeval>current:
        diff = datetimeval-current
        totalhours = diff.seconds/3600
        balance_hours_after_half_day = totalhours % 12
        balance_hours_after_quarter_day = balance_hours_after_half_day % 6
        #print 'balance_hours_after_quarter_day=',balance_hours_after_quarter_day
        return range(balance_hours_after_quarter_day)
    else:
        return []

@register.filter    
def halfhourslist(datetimeval):
    current = datetime.datetime.now()
    if datetimeval>current:
        diff = datetimeval-current
        balance_seconds = diff.seconds % 3600
        balance_minutes = balance_seconds / 60
        balance_half_hours = balance_minutes /30
        #print 'balance_half_hours=',balance_half_hours
        return range(balance_half_hours)
    else:
        return []
