from django import template
from subjects.models import Attendance,SquadCell,TimePeriod
from papers.models import Comment
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def day_cells(day, week):
    res = []
    for cell in day.day_cell.all():
        sc = SquadCell.objects.filter(week=week,cell=cell)
        if len(sc) > 0:
            res.append(sc)
    return res

@register.filter
def find_sc(subject_material, squad):
    return subject_material.material_cells.filter(squad=squad)

@register.filter
def find_attendance(squad_cell, subject):
    return squad_cell.attendances.filter(subject=subject)

@register.filter
def hisattendance(squad_cell, student):
    return squad_cell.attendances.filter(student=student)

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
def check_date(date, delta):
    if date > timezone.now().date():
        return 'future'
    elif date + timedelta(int(delta)) >= timezone.now().date():
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



