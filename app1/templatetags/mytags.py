from django import template
import datetime
register = template.Library()

@register.filter
def change_line(value):
    if value == '3':
        return 'Line3'
    elif value == '10':
        return 'Line10'
    else:
        pass

@register.filter
def change_status(value):
    if value == 1:
        return '故障'
    elif value == 2:
        return '待机'
    elif value == 3:
        return '检修'
    elif value == 4:
        return '运行'

@register.filter
def change_date(value):
    a = value.strftime('%Y-%m-%d \b\b %H:%M:%S')
    return a