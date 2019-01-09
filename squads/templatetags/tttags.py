from django import template
from subjects.models import TimePeriod, SquadCell
register = template.Library()

@register.filter
def week_dates(week):
    res = []
    timep = TimePeriod.objects.all()[0]
    for sc in SquadCell.objects.filter(week = week, time_period=timep):
        res.append(sc)
    return res

@register.filter
def time_cells(week, timep):
    return SquadCell.objects.filter(week = week, time_period=timep)