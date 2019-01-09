from django import template
from subjects.models import Attendance,SquadCell,TimePeriod
from papers.models import Comment
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