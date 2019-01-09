from django import template
from ..models import SquadCell, Lecture
register = template.Library()

@register.filter
def findorder(material, profile):
    for sq in profile.squads.all():
        llist = SquadCell.objects.filter(squad = sq, subject_materials=material)
        if len(llist)>0:
            res = str(llist[0].date.strftime('%d %B %Y')) + 'г. ' + llist[0].time_period.start +'-'+ llist[0].time_period.end
            return [llist[0].date, ' Время: ' + llist[0].time_period.start +'-'+ llist[0].time_period.end]
    return 'de'

@register.filter
def cell_subject_lectures(cell, subject):
    return Lecture.objects.filter(subject =subject, cell = cell)
