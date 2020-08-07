from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView

from .forms import TaskForm
from .models import *
from accounts.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse
from constants import *

class ChangeTimeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, slug=None, format=None):
        data = {
        }
        return Response(data)
                
def ChangeAnswer(request):
    profile = Profile.objects.get(user = request.user.id)
    solved = False
    was_solved = False
    parent = True
    action = ''
    value = 0
    print(request.GET.get('id'))
    print(request.GET.get('ans'))
    if request.GET.get('id'):
        task = Task.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('ans'):
            answer = request.GET.get('ans').split('@')
            print(answer, task.answer)
            del answer[-1]
            answer = sorted(answer)
            if profile.is_student:
                solver_checks = task.solver_checks.get(author_profile=profile)
                was_solved = solver_checks.solver_correctness
                solver_checks.solver_correctness = False
                solver_checks.solver_try_number += 1
                solved = False
                if sorted(task.answer) == answer:
                    solver_checks.solver_correctness = True
                    solved = True
                    for child in task.children.all():
                        child_solver_checks = child.solver_checks.get(author_profile=profile)
                        if child_solver_checks == False:
                            solver_checks.solver_correctness = False
                            solved = False
                            break
                    if solved:
                        if was_solved == False:
                            profile.coins += task.cost
                            action = 'plus'
                            value = task.cost
                            for tag in task.tags.all():
                                tag_id = tag.id
                                if len(Skill.objects.filter(author=profile)) == 0:
                                    skill = Skill.objects.create()
                                    skill.author = profile
                                    skill.save()
                                if not tag_id in profile.skill.tag_ids:
                                    profile.skill.tag_ids.append(tag_id)
                                    profile.skill.easy_skills.append(0)
                                    profile.skill.middle_skills.append(0)
                                    profile.skill.hard_skills.append(0)
                                    profile.skill.pro_skills.append(0)
                                index = profile.skill.tag_ids.index(tag_id)
                                if task.cost <= 2:
                                    profile.skill.easy_skills[index] += task.cost
                                elif task.cost <= 10:
                                    profile.skill.middle_skills[index] += task.cost
                                elif task.cost <= 25:
                                    profile.skill.hard_skills[index] += task.cost
                                else:
                                    profile.skill.pro_skills[index] += task.cost
                                profile.save()
                else:
                    if was_solved:
                        profile.coins -= task.cost
                        action = 'minus'
                        value = task.cost
                solver_checks.solver_ans = answer
                solver_checks.save()
                # task_parent = task.parent
                # if task_parent:
                #     parent_solver_checks = task_parent.solver_checks.get(author_profile=profile)
                #     was_parent_solved = parent_solver_checks.solver_correctness
                #     if solved == False:
                #         if was_parent_solved:
                #             profile.coins -= task_parent.cost
                #             value = task_parent.cost
                #             action = 'minus'
                #         parent_solver_checks.solver_correctness = False
                #         parent = False
                #     else:
                #         parent_solver_checks.solver_correctness = True
                #         for task_brother in task_parent.children():
                #             brother_solver_checks = task_brother.solver_checks.get(author_profile=profile)
                #             if brother_solver_checks.solver_correctness == False:
                #                 brother_solver_checks.solver_correctness = False
                #                 if was_parent_solved:
                #                     profile.coins -= task_parent.cost
                #                     value = task_parent.cost
                #                     action = 'minus'
                #                 parent = False
                #                 break
                #             task_brother.save()
                #             brother_solver_checks.save()
                #     task_parent.save()
                #     parent_solver_checks.save()
                # else:
                #     parent = 'no_parent'
    profile.save()
    task.save()
    data = {
        'solved':solved,
        # 'parent':parent,
        'action':action,
        'hiscoins':profile.coins,
    }
    return JsonResponse(data)

def ChangeText(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('id') and is_profi(profile, 'Teacher'):
        task = Task.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('text'):
            task.text = request.GET.get('text')
        if request.GET.get('cost'):
            task.cost = request.GET.get('cost')
        if request.GET.get('answer'):
            answer = request.GET.get('answer').split('&')
            del answer[-1]
            task.answer = answer
        task.save()
    data = {
    }
    return JsonResponse(data)


def task_delete(request):
    if request.GET.get('id'):
        task = Task.objects.get(id = int(request.GET.get('id')))
        task.delete()
                    
    data = {
        "like_num":0,
    }
    return JsonResponse(data)

