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
from tasks.models import Task, ProblemTag
from squads.models import Squad
from papers.models import Comment
from library.models import Folder
from accounts.models import *
from constants import *

def lesson_details(request, lesson_id = None):
    profile = get_profile(request)
    lesson = Lesson.objects.get(id=lesson_id)
    if len(lesson.papers.all()) == 0:
        return redirect(lesson.estimate_lesson_page())
    else:
        for paper in lesson.papers.all():
            if not profile in paper.done_by.all():
                return redirect(paper.get_absolute_url())

def estimate_lesson_page(request, lesson_id = None):
    profile = get_profile(request)
    lesson = Lesson.objects.get(id=lesson_id)
    is_in_school(profile, lesson.school)           
    if not profile.id in lesson.estimater_ids:
        lesson.estimater_ids.append(profile.id)
        lesson.grades.append(0)
    index = lesson.estimater_ids.index(profile.id)
    context = {
        "profile": profile,
        'lesson':lesson,
        'hisestimation':lesson.grades[index],
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":profile.schools.first().money,
    }
    return render(request, template_name='library/lesson_details.html', context=context)

def paper_details(request, paper_id = None):
    profile = get_profile(request)
    paper = Paper.objects.get(id=paper_id)
    lesson = paper.lessons.first()
    is_in_school(profile, lesson.school)           
    subtheme_text_form = SubthemeTextForm(request.POST or None)
    if subtheme_text_form.is_valid():
        subtheme = subtheme_text_form.save(commit=False)
        subtheme.save()
        paper_id = request.POST.get('paper_id')
        paper = Paper.objects.get(id = int(paper_id))
        paper.subthemes.add(subtheme)
        return redirect(paper.get_absolute_url())

    subtheme_file_form = SubthemeFileForm(request.POST or None, request.FILES or None)
    if subtheme_file_form.is_valid():
        subtheme = subtheme_file_form.save(commit=False)
        subtheme.save()
        paper_id = request.POST.get('paper_id')
        paper = Paper.objects.get(id = int(paper_id))
        paper.subthemes.add(subtheme)
        return redirect(paper.get_absolute_url())

    subtheme_video_form = SubthemeVideoForm(request.POST or None, request.FILES or None)
    if subtheme_video_form.is_valid():
        subtheme = subtheme_video_form.save(commit=False)
        subtheme.youtube_video_link = subtheme.youtube_video_link.replace('watch?v=', 'embed/')
        subtheme.save()
        paper_id = request.POST.get('paper_id')
        paper = Paper.objects.get(id = int(paper_id))
        paper.subthemes.add(subtheme)
        return redirect(paper.get_absolute_url())
    is_director = False
    if is_profi(profile, 'Director'):
        is_director = True
    context = {
        "profile": profile,
        'lesson':lesson,
        'paper':paper,
        'subtheme_text_form':subtheme_text_form,
        'subtheme_file_form':subtheme_file_form,
        'subtheme_video_form':subtheme_video_form,
        'tasks':Task.objects.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_director,
        "school_money":profile.schools.first().money,
    }
    return render(request, "library/lesson_details.html", context)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def add_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('paper_id') and request.GET.get('group_id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('paper_id')))
        is_in_school(profile, lesson.school)           
        course = Course.objects.get(id = int(request.GET.get('group_id')))
        course.lessons.add(lesson)
    data = {
    }
    return JsonResponse(data)

def AddPaper(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('id')))
        is_in_school(profile, lesson.school)           
        if request.GET.get('title'):
            paper = Paper.objects.create(title=request.GET.get('title'),school=lesson.school)
            subtheme = Subtheme.objects.create()
            subtheme.save()
            paper.subthemes.add(subtheme)
            lesson.papers.add(paper)
        paper.author_profile = profile
        paper.save()
    data = {
    }
    return JsonResponse(data)

def AddSubtheme(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        paper = Paper.objects.get(id = int(request.GET.get('id')))
        is_in_school(profile, paper.school)           
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

def NewTask(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('text') and request.GET.get('cost') and request.GET.get('subtheme_id'):
        task = Task.objects.create(author_profile=profile, text=request.GET.get('text'))
        if request.GET.get('ans') != '&':
            task.answer = request.GET.get('ans').split('&')
            del task.answer[-1]
        elif request.GET.get('variants'):
            task.answer = request.GET.get('variant_ans').split('&')
            del task.answer[-1]
            task.variants = request.GET.get('variants').split('&')
            del task.variants[-1]
            if task.variants[0] != '':
                task.is_test = True
                if len(task.answer) > 1:
                    task.is_mult_ans = True
        if request.GET.get('tags') != '':
            tags = request.GET.get('tags').split('&')
            del tags[-1]
            # print(tags)
            for t in tags:
                tag = ProblemTag.objects.get_or_create(title=t)[0]
                task.tags.add(tag)
        
        subtheme = Subtheme.objects.get(id=int(request.GET.get('subtheme_id')))
        is_in_school(profile, subtheme.papers.first().school)           
        task.subthemes.add(subtheme)                    
        task.cost = request.GET.get('cost')
        task.save()
    data = {
        "delete_url":task.get_delete_url(),
        'id':task.id,
        'change_text_url':task.change_text_url(),
        'change_answer_url':task.change_answer_url(),
    }
    return JsonResponse(data)

def AddTask(request):
    action = ''
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('subtheme_id') and request.GET.get('task_id'):
        subtheme = Subtheme.objects.get(id = int(request.GET.get('subtheme_id')))
        is_in_school(profile, subtheme.papers.first().school)           
        task = Task.objects.get(id = int(request.GET.get('task_id')))
        if task in subtheme.task_list.all():
            subtheme.task_list.remove(task)
            action = 'remove'
        else:
            subtheme.task_list.add(task)
            action = 'add'
    data = {
        'action': action
    }
    return JsonResponse(data)

def create_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    name = 'Урок'
    if request.GET.get('school_id'):
        school = School.objects.get(id=int(request.GET.get('school_id')))
        is_in_school(profile, school)           
        if len(school.lessons.all()) > 0:
            name += str(school.lessons.all()[len(school.lessons.all())-1].id + 1)
    lesson = Lesson.objects.create(title = name, author_profile = profile)
    if request.GET.get('school_id'):
        lesson.school = school
    lesson.save()
    if request.GET.get('parent_id') != 'denone':
        parent = Folder.objects.get(id = int(request.GET.get('parent_id')))
        parent.lesson_list.add(lesson)
    data = {}
    return JsonResponse(data)        

def rename_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id') and request.GET.get('name'):
        lesson = Lesson.objects.get(id = int(request.GET.get('id')))
        is_in_school(profile, lesson.school)           
        lesson.title = request.GET.get('name')
        lesson.save()

    data = {}
    return JsonResponse(data)

def rename_paper(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('new_title') and request.GET.get('id'):
        if len(request.GET.get('new_title')) > 0:
            paper = Paper.objects.get(id = int(request.GET.get('id')))
            is_in_school(profile, paper.school)           
            if paper.title != request.GET.get('new_title'):
                paper.title = request.GET.get('new_title')
                paper.save()
    data = {}
    return JsonResponse(data)

def rewrite_subtheme(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('new_content') and request.GET.get('id'):
        if len(request.GET.get('new_content')) > 0:
            subtheme = Subtheme.objects.get(id = int(request.GET.get('id')))
            is_in_school(profile, subtheme.papers.first().school)
            if subtheme.content != request.GET.get('new_content'):
                subtheme.content = request.GET.get('new_content')
                subtheme.save()
    data = {}
    return JsonResponse(data)

def delete_paper(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        paper = Paper.objects.get(id = int(request.GET.get('id')))
        is_in_school(profile, paper.school)
        paper.delete()
    data = {}
    return JsonResponse(data)

def rename_subtheme(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('new_title') and request.GET.get('id'):
        if len(request.GET.get('new_title')) > 0:
            subtheme = Subtheme.objects.get(id = int(request.GET.get('id')))
            is_in_school(profile, subtheme.papers.first().school)
            if subtheme.title != request.GET.get('new_title'):
                subtheme.title = request.GET.get('new_title')
                subtheme.save()
    data = {}
    return JsonResponse(data)

def delete_subtheme(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        subtheme = Subtheme.objects.get(id = int(request.GET.get('id')))
        is_in_school(profile, subtheme.papers.first().school)
        subtheme.delete()
    data = {}
    return JsonResponse(data)

def delete_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('id')))
        is_in_school(profile, lesson.school)
        lesson.delete()
    data = {}
    return JsonResponse(data)

def delete_course(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        course = Course.objects.get(id = int(request.GET.get('id')))
        is_in_school(profile, course.school)
        course.delete()
    data = {}
    return JsonResponse(data)

def AddGroup(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
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

def estimate_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('new_rating') and request.GET.get('lesson_id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('lesson_id')))
        is_in_school(profile, lesson.school)
        if not profile.id in lesson.estimater_ids:
            lesson.estimater_ids.append(profile.id)
            lesson.grades.append(1)
        index = lesson.estimater_ids.index(profile.id)
        lesson.grades[index] = int(request.GET.get('new_rating'))
        grades_sum = 0
        for grade in lesson.grades:
            grades_sum += grade
        if len(lesson.grades) > 0:
            lesson.rating = int(grades_sum/len(lesson.grades))
        else:
            lesson.rating = 0
        lesson.save()
        
    data = {
    }
    return JsonResponse(data)

def courses(request):
    profile = ''
    is_trener = ''
    is_manager = ''
    is_director = ''
    if request.user.is_authenticated:
        profile = get_profile(request)
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
    context = {
        "profile": profile,
        "course_sets":course_sets(),
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director,
        "school_money":profile.schools.first().money,
    }
    return render(request, 'courses/course_list.html', context=context)

def course_sets():
    course_sets = []
    tops = ['Курсы с лучшими рейтингами']
    tops.append(package_courses('rating'))
    news = ['Свежие курсы']
    news.append(package_courses('-id'))
    course_sets.append(tops)
    course_sets.append(news)
    return course_sets

def package_courses(order_item):
    index = 0
    sets = []
    temp_set = []
    for course in Course.objects.all().order_by(order_item):
        index += 1
        temp_set.append(course)
        if index % 4 == 0:
            sets.append(temp_set)
            temp_set = []
        if index == 12:
            break
    if index < 12:
        sets.append(temp_set)
    return sets

def course_details(request, course_id=None):
    profile = get_profile(request)
    course = Course.objects.get(id=course_id)
    if not is_profi(profile, 'CEO') and not is_profi(profile, 'Creator'):
        if not profile in course.students.all():
            raise Http404

    lessons = []
    folders = []
    for school in profile.schools.all():
        lessons += list(school.lessons.all())
        folders += list(school.school_folders.all())
    lessons += Lesson.objects.filter(access_to_everyone=True)
    lessons = set(lessons)
    context = {
        "profile": profile,
        "course":course,
        "lessons":lessons,
        "folders":folders,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":profile.schools.first().money,
    }
    return render(request, 'courses/course_details.html', context=context)

def course_seller(request, course_id=None):
    profile = get_profile(request)
   
    context = {
        "profile": profile,
        "course":Course.objects.get(id=course_id),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'), 
        "school_money":profile.schools.first().money,
    }
    return render(request, 'courses/course_seller.html', context=context)

def course_update(request, course_id=None):
    profile = get_profile(request)
    course = get_object_or_404(Course, id=course_id)
    is_in_school(profile, course.school)
    form = CourseForm(request.POST or None, request.FILES or None, instance=course)
    if form.is_valid():
        course = form.save(commit=False)
        if not course.height_field:
            course.height_field = 0
        if not course.width_field:
            course.width_field = 0
        course.save()
        return HttpResponseRedirect(course.get_update_url())
    context = {
        "course": course,
        "form":form,
        'page':'course_update',
        "profile":profile,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'), 
        "school_money":profile.schools.first().money,
    }
    return render(request, "courses/course_create.html", context)

def course_create(request):
    profile = get_profile(request)        
    form = CourseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        course = form.save(commit=False)
        course.author_profile = profile
        course.school = profile.schools.first()
        course.save()
        return HttpResponseRedirect(course.get_absolute_url())

    context = {
        "form": form,
        "profile":profile,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'), 
        "school_money":profile.schools.first().money,
    }
    return render(request, "courses/course_create.html", context)

def pay_for_course(request):
    if request.GET.get('course_id'):
        ok = False
        profile = Profile.objects.get(user = request.user.id)
        course = Course.objects.get(id = int(request.GET.get('course_id')))
        if profile.coins > course.cost:
            course.students.add(profile)
            profile.coins -= course.cost
            profile.save()
            ok = True

    data = {
        "ok":ok
    }
    return JsonResponse(data)

def check_paper(request):
    if request.GET.get('current_paper'):
        profile = Profile.objects.get(user = request.user.id)
        paper = Paper.objects.get(id = int(request.GET.get('current_paper')))
        
        solver_correctness = True
        for subtheme in paper.subthemes.all():
            for task in subtheme.task_list.all():
                solver = profile.check_tasks.get_or_create(task = task)[0]
                if solver.solver_correctness == False:
                    solver_correctness = False
                    break
        if solver_correctness:
            paper.done_by.add(profile)
            lesson = paper.lessons.first()
            lesson_is_done = True
            for ppr in lesson.papers.all():
                if not profile in ppr.done_by.all():
                    lesson_is_done = False
                    break
            if lesson_is_done:
                lesson.done_by.add(profile)
        else:
            paper.done_by.remove(profile)
    data = {
        'is_solved': solver_correctness
    }
    return JsonResponse(data)
