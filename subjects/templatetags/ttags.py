from django import template
from ..models import SquadCell, Lecture
register = template.Library()
from django.utils import timezone

@register.filter
def findorder(material, profile):
    llist = profile.squads.first().cells.filter(subject_materials=material)
    if len(llist)>0:
        return [llist[0].date, ' ' + llist[0].time_period.start +'-'+ llist[0].time_period.end]
    return 'de'

@register.filter
def check_material_date(material, profile):
    llist = profile.squads.first().cells.filter(subject_materials=material)
    if len(llist)>0:
        date = llist[0].date
        if date < timezone.now().date():
            return True
    return False

@register.filter
def cell_subject_lectures(cell, subject):
    return Lecture.objects.filter(subject =subject, cell = cell)
