'''
Created on Oct 14, 2012

@author: sajan
'''
from django import template
from django.conf import settings

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