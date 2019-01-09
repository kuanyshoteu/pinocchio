from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView

from .forms import *
from .models import *
from tasks.models import Task
from squads.models import Squad
from papers.models import Comment
from library.models import Folder
from accounts.models import *

def lesson_details(request, lesson_id = None):
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    else:
        raise Http404

    lesson = Lesson.objects.get(id=lesson_id)
    subtheme_form = SubthemeForm(request.POST or None, request.FILES or None)
    if subtheme_form.is_valid():
        subtheme = subtheme_form.save(commit=False)
        subtheme.youtube_video_link = subtheme.youtube_video_link.replace('watch?v=', 'embed/')
        subtheme.save()

        paper_id = request.POST.get('paper_id')
        paper = Paper.objects.get(id = int(paper_id))
        paper.subthemes.add(subtheme)

        return redirect(lesson.get_absolute_url())

    context = {
        "profile": profile,
        'lesson':lesson,
        'subtheme_form':subtheme_form,
        'tasks':Task.objects.all(),
    }
    return render(request, template_name='library/lesson_details.html', context=context)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def add_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    if profile.is_trener:
        if request.GET.get('paper_id') and request.GET.get('group_id'):
            lesson = Lesson.objects.get(id = int(request.GET.get('paper_id')))
            course = Course.objects.get(id = int(request.GET.get('group_id')))
            course.lessons.add(lesson)
    data = {
    }
    return JsonResponse(data)

def AddPaper(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('title'):
            paper = Paper.objects.create(title=request.GET.get('title'))
            lesson.papers.add(paper)
        paper.author_profile = profile
        paper.save()
    data = {
    }
    return JsonResponse(data)

def AddSubtheme(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('id'):
        paper = Paper.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('title'):
            subtheme = Subtheme.objects.create(title=request.GET.get('title'))
            paper.subthemes.add(subtheme)
        if request.GET.get('content'):
            subtheme.content = request.GET.get('content')     
        if request.GET.get('videolink'):
            subtheme.video_link = request.GET.get('videolink').replace('watch?v=', 'embed/')
      
        subtheme.save()
    data = {
    }
    return JsonResponse(data)

def AddTask(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('text'):
        if request.GET.get('ans'):
            task = Task.objects.create(author_profile=profile, text=request.GET.get('text'), answer = request.GET.get('ans').split(';'))
            del task.answer[-1]
        if request.GET.get('variants'):
            task.variants = request.GET.get('variants').split(';')
            del task.variants[-1]
            if task.variants[0] != '':
                task.is_test = True
                if len(task.answer) > 1:
                    task.is_mult_ans = True
        if request.GET.get('subtheme_id'):
            subtheme = Subtheme.objects.get(id=int(request.GET.get('subtheme_id')))
            task.subthemes.add(subtheme)                    
        if request.GET.get('cost'):
            task.cost = request.GET.get('cost')

        task.save()
    data = {
        "delete_url":task.get_delete_url(),
        'id':task.id,
        'change_text_url':task.change_text_url(),
        'change_answer_url':task.change_answer_url(),
    }
    return JsonResponse(data)

def create_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    if len(Lesson.objects.all()) > 0:
        name = 'Новый список' + str(Lesson.objects.all()[len(Lesson.objects.all())-1].id + 1)
    else:
        name = 'Новая список'
    lesson = Lesson.objects.create(title = name, author_profile = profile)
    lesson.save()
    if request.GET.get('parent_id') != 'denone':
        parent = Folder.objects.get(id = int(request.GET.get('parent_id')))
        parent.lesson_list.add(lesson)
    data = {}
    return JsonResponse(data)        

def rename_lesson(request):
    if request.GET.get('id'):
        if request.GET.get('id') == 'new_paper':
            lesson = Lesson.objects.all()[0]
        else:
            lesson = Lesson.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('name'):
            lesson.title = request.GET.get('name')
            lesson.save()

    data = {}
    return JsonResponse(data)

def rename_paper(request):
    if request.GET.get('new_title') and request.GET.get('id'):
        if len(request.GET.get('new_title')) > 0:
            paper = Paper.objects.get(id = int(request.GET.get('id')))
            if paper.title != request.GET.get('new_title'):
                paper.title = request.GET.get('new_title')
                paper.save()
    data = {}
    return JsonResponse(data)

def rewrite_subtheme(request):
    if request.GET.get('new_content') and request.GET.get('id'):
        if len(request.GET.get('new_content')) > 0:
            subtheme = Subtheme.objects.get(id = int(request.GET.get('id')))
            if subtheme.content != request.GET.get('new_content'):
                subtheme.content = request.GET.get('new_content')
                subtheme.save()
    data = {}
    return JsonResponse(data)

def delete_paper(request):
    if request.GET.get('id'):
        paper = Paper.objects.get(id = int(request.GET.get('id')))
        paper.delete()
    data = {}
    return JsonResponse(data)

def rename_subtheme(request):
    if request.GET.get('new_title') and request.GET.get('id'):
        if len(request.GET.get('new_title')) > 0:
            subtheme = Subtheme.objects.get(id = int(request.GET.get('id')))
            if subtheme.title != request.GET.get('new_title'):
                subtheme.title = request.GET.get('new_title')
                subtheme.save()
    data = {}
    return JsonResponse(data)

def delete_subtheme(request):
    if request.GET.get('id'):
        subtheme = Subtheme.objects.get(id = int(request.GET.get('id')))
        subtheme.delete()
    data = {}
    return JsonResponse(data)

def delete_lesson(request):
    if request.GET.get('id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('id')))
        lesson.delete()
    data = {}
    return JsonResponse(data)

def delete_course(request):
    if request.GET.get('id'):
        course = Course.objects.get(id = int(request.GET.get('id')))
        course.delete()
    data = {}
    return JsonResponse(data)

def AddGroup(request):
    if request.GET.get('paper_id') and request.GET.get('squad_id') and request.GET.get('isin'):
        squad = Squad.objects.get(id = request.GET.get('squad_id')) 
        paper = Paper.objects.get(id = request.GET.get('paper_id'))
        if request.GET.get('isin') == 'yes' and squad in paper.squad_list.all():
            paper.squad_list.remove(squad)
        if request.GET.get('isin') == 'no' and not squad in paper.squad_list.all():
            paper.squad_list.add(squad)
    data = {
    }
    return JsonResponse(data)

def new_comment(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('content') and request.GET.get('lesson_id') and request.GET.get('parent_id'):
        comment = Comment.objects.create(
            content = request.GET.get('content'),
            lesson = Lesson.objects.get(id=int(request.GET.get('lesson_id'))),
            author_profile = profile,
            )
        parent_id = int(request.GET.get('parent_id'))
        if parent_id > 0:
            parent = Comment.objects.get(id=parent_id)
            comment.parent = parent
            comment.level = parent.level + 1
            comment.save()

    data = {}
    return JsonResponse(data)

def like_comment(request):
    profile = Profile.objects.get(user = request.user.id)
    like = False
    if request.GET.get('id'):
        comment = Comment.objects.get(id=int(request.GET.get('id')))
        if profile in comment.dislikes.all():
            comment.dislikes.remove(profile) 
        else:
            comment.likes.add(profile)
            like = True
    res = len(comment.likes.all()) - len(comment.dislikes.all())
    if res > 0:
        res = "+" + str(res)
    data = {
        "like_num":res,
        "like":like,
    }
    return JsonResponse(data)

def dislike_comment(request):
    profile = Profile.objects.get(user = request.user.id)
    dislike = False
    if request.GET.get('id'):
        comment = Comment.objects.get(id=int(request.GET.get('id')))
        if profile in comment.likes.all():
            comment.likes.remove(profile)
        else:
            comment.dislikes.add(profile)
            dislike = True
    res = len(comment.likes.all()) - len(comment.dislikes.all())
    data = {
        "like_num":res,
        "dislike":dislike,
    }
    return JsonResponse(data)

def like_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    like = False
    if request.GET.get('id'):
        lesson = Lesson.objects.get(id=int(request.GET.get('id')))
        if profile in lesson.dislikes.all():
            lesson.dislikes.remove(profile) 
        else:
            lesson.likes.add(profile)
            like = True
    res = len(lesson.likes.all()) - len(lesson.dislikes.all())
    if res > 0:
        res = "+" + str(res)
    data = {
        "like_num":res,
        "like":like,
    }
    return JsonResponse(data)

def dislike_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    dislike = False
    if request.GET.get('id'):
        lesson = Lesson.objects.get(id=int(request.GET.get('id')))
        if profile in lesson.likes.all():
            lesson.likes.remove(profile)
        else:
            lesson.dislikes.add(profile)
            dislike = True
    res = len(lesson.likes.all()) - len(lesson.dislikes.all())
    data = {
        "like_num":res,
        "dislike":dislike,
    }
    return JsonResponse(data)

def course_details(request, course_id=None):
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    else:
        raise Http404
   
    context = {
        "profile": profile,
        "course":Course.objects.get(id=course_id),
        'lessons':Lesson.objects.all(),
        "folders":Folder.objects.all(),
    }
    return render(request, 'courses/course_details.html', context=context)

def course_seller(request, course_id=None):
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    else:
        raise Http404
   
    context = {
        "profile": profile,
        "course":Course.objects.get(id=course_id),
    }
    return render(request, 'courses/course_seller.html', context=context)

def course_update(request, course_id=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    course = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, request.FILES or None, instance=course)
    if form.is_valid():
        course = form.save(commit=False)
        if not course.height_field:
            course.height_field = 0
        if not course.width_field:
            course.width_field = 0
        course.save()
        return HttpResponseRedirect(course.get_update_url())
        
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

    context = {
        "course": course,
        "form":form,
        'page':'course_update',
        "profile":profile,
    }
    return render(request, "courses/course_create.html", context)

def course_create(request):
    if not request.user.is_authenticated:
        raise Http404

    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    if not profile.is_trener:
        raise Http404
        
    form = CourseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        course = form.save(commit=False)
        course.save()
        return HttpResponseRedirect(course.get_absolute_url())

    context = {
        "form": form,
        "profile":profile,
    }
    return render(request, "courses/course_create.html", context)

def rename_course(request):
    if request.GET.get('id'):
        if request.GET.get('id') == 'new_course':
            course = Course.objects.all()[0]
        else:
            course = Course.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('name'):
            course.title = request.GET.get('name')
            course.save()

    data = {}
    return JsonResponse(data)

def check_paper(request):
    if request.GET.get('current_paper'):
        profile = Profile.objects.get(user = request.user.id)
        paper = Paper.objects.get(id = int(request.GET.get('current_paper')))
        paper_solver = profile.check_papers.get_or_create(paper=paper)[0]
        paper_solver.solver_correctness = True
        for subtheme in paper.subthemes.all():
            for task in subtheme.task_list.all():
                solver = profile.check_tasks.get_or_create(task = task)[0]
                if solver.solver_correctness == False:
                    paper_solver.solver_correctness = False
                    break
        paper_solver.save()
    data = {
        'is_solved': paper_solver.solver_correctness
    }
    return JsonResponse(data)
