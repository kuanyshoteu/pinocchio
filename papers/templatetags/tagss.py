from django import template
from tasks.models import Solver
register = template.Library()

@register.filter
def is_correct(task, profile):
    return task.solver_checks.get_or_create(author_profile=profile)[0].solver_correctness

@register.filter
def is_done(paper, profile):
    if profile in paper.done_by.all():
        return True
    else:
        return False

@register.filter
def addstr(str1, str2):
    return str(str1) + str(str2)

@register.filter
def hisanswers(task, profile):
    return task.solver_checks.get_or_create(author_profile=profile)[0].solver_ans

@register.filter
def hisanswer(task, profile):
    return task.solver_checks.get_or_create(author_profile=profile)[0].solver_ans[0]