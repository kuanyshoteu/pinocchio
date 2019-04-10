from django import template
from subjects.models import Attendance,TimePeriod
from papers.models import Comment
from django.utils import timezone
from datetime import timedelta
from subjects.templatetags.ttags import get_date

register = template.Library()

@register.filter
def minus(x):
    return int(x) - 4

@register.filter
def is_odd(number):
    if number % 2 == 0:
        return False
    else:
        return True

@register.filter
def check_date(material, squad):
    date = get_date(material, squad)
    if date > timezone.now().date():
        return 'future'
    elif date + timedelta(7) >= timezone.now().date():
        return 'now'
    else:
        return 'past'
        
@register.filter
def get_children(comment):
    res = []
    for cm in Comment.objects.filter(parent=comment):
        if cm != comment:
            cm.level = comment.level + 1
            cm.save()
            res.append(cm)
    return res

@register.filter
def count_likes(comment):
    res = len(comment.likes.all()) - len(comment.dislikes.all())
    if res > 0:
        res = "+" + str(res)
    return res

@register.filter
def in_percent(number):
    if number > 0:
        return str(number/1000) + ',100'
    else:
        return '0,100'

@register.filter
def top_students(school):
    res = []
    for student in school.students.all():
        if len(res) == 7:
            break
        if not student.is_trener:
            res.append(student)
    return res

@register.filter
def top_teachers(school):
    return school.students.filter(is_trener=True)

@register.filter
def module_six(number):
    return number % 6

@register.filter
def find_time_by_num(number):
    tp = TimePeriod.objects.get(num = number)
    return tp.start + '-' + tp.end

@register.filter
def find_by_index(array, index):
    return array[index]
