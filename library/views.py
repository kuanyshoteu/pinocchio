from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView

from accounts.models import *
from papers.models import *
from .models import *
from django.contrib.auth.models import User
from constants import *

def library(request):
    profile = get_profile(request)
    only_staff(profile)
    school = profile.schools.first()
    return redirect(school.get_school_library())

def school_library(request, school_id):
    profile = get_profile(request)
    school = School.objects.get(id=school_id)
    is_in_school(profile, school)        

    context = {
        "profile": profile,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "page":'library',
        "school_crnt":school,
    }
    return render(request, 'library/library.html', context=context)

def folder_details(request, folder_id=None):
    profile = get_profile(request)
    only_teachers(profile)
    folder = Folder.objects.get(id=folder_id)
    school = folder.school
    is_in_school(profile, folder.school)        
    context = {
        "profile": profile,
        'folder':folder,
        'cache':Cache.objects.get_or_create(author_profile = profile)[0],
        'lessons':folder.lesson_list.all(),
        'folders':folder.children.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'), 
        "school_money":profile.schools.first().money,
        "current_school_id":school.id,
        "page":'library',        
        "school_crnt":school,
    }
    return render(request, 'library/library.html', context=context)

from django.http import JsonResponse
def file_action(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    cache = Cache.objects.get_or_create(author_profile = profile)
    cache = cache[0]
    
    cache.object_type = request.GET.get('object_type')
    cache.object_id = int(request.GET.get('object_id'))
    cache.action = request.GET.get('action')
    cache.previous_parent = int(request.GET.get('parent'))
    cache.full = True
    cache.save()
    data = {'status':'ok'}
    return JsonResponse(data)

def paste(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    cache = Cache.objects.get_or_create(author_profile = profile)[0]
    title = ''
    link = ''
    if request.GET.get('new_parent') != 'library':
        new_parent = Folder.objects.get(id = int(request.GET.get('new_parent')))
        school = new_parent.school
    elif request.GET.get('school_id'):
        school = School.objects.get(id=int(request.GET.get('school_id')))
    is_in_school(profile, school)
    if cache.object_type == 'folder':    
        folder = Folder.objects.get(id = cache.object_id)
        title = folder.title
        link = folder.get_absolute_url()
        copy_folder = Folder.objects.create(author_profile = profile, title=folder.title, school=folder.school)
        for ppr in folder.lesson_list.all():
            copy_folder.lesson_list.add(ppr)
        if request.GET.get('new_parent') != 'library':
            copy_folder.parent = new_parent
            new_parent.children.add(copy_folder)
        elif request.GET.get('school_id'):
            copy_folder.school = school
        copy_folder.save()
        if cache.action == 'cut' and cache.previous_parent > 0:
            folder.delete()
    if cache.object_type == 'lesson':
        lesson = Lesson.objects.get(id = cache.object_id)
        new_lesson = Lesson.objects.create(author_profile = profile, title = lesson.title, school=lesson.school)
        new_lesson.save()
        title = new_lesson.title
        link = new_lesson.get_absolute_url()
        for paper in lesson.papers.all():
            new_paper = new_lesson.papers.create(title=paper.title,
                author_profile=paper.author_profile, typee=paper.typee)
            for subtheme in paper.subthemes.all():
                new_subtheme = Subtheme.objects.create(content=subtheme.content,video=subtheme.video,
                    youtube_video_link=subtheme.youtube_video_link)
                new_paper.subthemes.add(new_subtheme)
                for task in subtheme.task_list.all():
                    new_task = Task.objects.create(
                        author_profile = profile, 
                        text = task.text, 
                        answer = task.answer)
                    if task.image:
                        new_task.image = task.image
                    new_task.save()
                    new_subtheme.task_list.add(new_task)

        if request.GET.get('new_parent') != 'library':
            new_parent.lesson_list.add(new_lesson)
        elif request.GET.get('school_id'):
            new_lesson.school = school
        if cache.action == 'cut':
            lesson.delete()
    data = {
        'status':'ok',
        'object_type':cache.object_type,
        'title':title,
        'link':link,
    }
    return JsonResponse(data)
    

def create_folder(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('title') and request.GET.get('parent_id'):
        school = is_moderator_school(request, profile)
        folder = school.lesson_folders.create(
            title = request.GET.get('title'),
            author_profile = profile,
            )
        if request.GET.get('parent_id') != '-1':
            parent = LessonFolder.objects.get(id = int(request.GET.get('parent_id')))
            folder.parent = parent
        folder.save()
        folder_id = folder.id
    data = {
        "id":folder_id
    }
    return JsonResponse(data)

def rename_folder(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    ok = False
    if request.GET.get('id') and request.GET.get('title'):
        school = is_moderator_school(request, profile)
        folder = school.lesson_folders.get(id = int(request.GET.get('id')))
        folder.title = request.GET.get('title')
        folder.save()
        ok = True
    data = {
        "ok":ok,
    }
    return JsonResponse(data)

def delete_folder(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    ok = False
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        folder = school.lesson_folders.get(id = int(request.GET.get('id')))
        folder.childs.all().delete()
        folder.lessons.all().delete()
        folder.delete()
        ok = True
    data = {
        "ok":ok,
    }
    return JsonResponse(data)

def get_library(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    folders = []
    lessons = []
    school = is_moderator_school(request, profile)
    for folder in school.lesson_folders.all():
        if not folder.parent:
            parent = -1
        else:
            parent = folder.parent.id
        folders.append([folder.id, folder.title, parent, len(folder.lessons.all())])
    lessons_q = school.lessons.filter(folder=None)
    lessons = fill_lessons(lessons_q)
    data = {
        'folders':folders,
        'lessons':lessons,
    }
    return JsonResponse(data)

def get_folder_files(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    lessons = []
    school = is_moderator_school(request, profile)
    if request.GET.get('id'):
        if request.GET.get('id') == '-1':
            lessons_q = school.lessons.filter(folder=None)
        else:
            folder = school.lesson_folders.filter(id = int(request.GET.get('id')))
            if len(folder) == 0:
                return JsonResponse({})
            folder = folder[0]
            lessons_q = folder.lessons.all()
        lessons = fill_lessons(lessons_q) 
    data = {
        'lessons':lessons,
    }
    return JsonResponse(data)

def fill_lessons(lessons_q):
    lessons = []
    for lesson in lessons_q:
        lessons.append([
            lesson.id,                          #0
            lesson.title,                       #1
            lesson.author_profile.first_name,   #2
            lesson.author_profile.get_absolute_url(),   #3
            lesson.rating,                      #4
            len(lesson.try_by.all()),           #5
            len(lesson.done_by.all()),          #6
            lesson.access_to_everyone,          #7
            lesson.get_absolute_url(),          #8
            ])    
    return lessons

def create_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    school = is_moderator_school(request, profile)
    ok = False
    if request.GET.get('parent') and request.GET.get('title'):
        lesson = school.lessons.create(
            title = request.GET.get('title'), 
            author_profile = profile,
            )
        if request.GET.get('parent') != '-1':
            folder = school.lesson_folders.get(id = int(request.GET.get('parent')))
            lesson.folder = folder
        lesson.save()
        paper = lesson.papers.create(title="Введение", school=school)
        paper.save()
        lessons = fill_lessons([lesson]) 
        ok = True
    data = {
        'lessons':lessons,
    }
    return JsonResponse(data)        

def collect_task(task, is_main, profile):
    task_res = []
    if task.image:
        image = task.image.url
    else:
        image = ''
    answer_type = 'text'
    if task.is_test:
        answer_type = 'test'
    if task.is_mult_ans:
        answer_type = 'multans'
    if is_profi(profile, 'Teacher'):
        answer = task.answer
        solver_correctness = False
    else:
        solver_checks = task.solver_checks.get_or_create(author_profile=profile)[0]
        answer = solver_checks.solver_ans
        solver_correctness = solver_checks.solver_correctness
    task_res = [
        task.id,        #0
        task.text,      #1
        image,          #2
        answer,         #3
        answer_type,    #4
        task.variants,  #5
        task.cost,      #6
        solver_correctness, #7
        ]
    if is_main:
        children = []
        for ctask in task.children.all():
            children.append(collect_task(ctask, False, profile))
        task_res.append(children)
    return task_res

def collect_paper(paper, profile):
    subthemes = []
    for subtheme in paper.subthemes.all():
        task_list = []
        if subtheme.task:
            task_list.append(collect_task(subtheme.task, True, profile))
        if subtheme.video:
            video = subtheme.video.url
        else:
            video = ''
        if subtheme.file:
            file = str(subtheme.file)
            file_url = subtheme.file.url
        else:
            file = ''
            file_url = ''
        subthemes.append([
            subtheme.id,                    #0
            subtheme.content,               #1
            file_url,                       #2
            file,                           #3
            subtheme.youtube_video_link,    #4
            video,                          #5
            task_list,                      #6
            ])
    res = [
        paper.id,
        paper.title,
        subthemes,
        ]    
    return res

def show_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    if request.GET.get('lesson_id') and request.GET.get('paper_id'):
        lesson = school.lessons.filter(id=int(request.GET.get('lesson_id')))
        if len(lesson) == 0:
            return JsonResponse({})
        lesson = lesson[0]
        paper_res = []
        if request.GET.get('paper_id') == '-1':
            paper = lesson.papers.filter(done_by=profile)
            if len(paper) > 0:
                paper = paper.first()
            else:
                paper = lesson.papers.first()
        else:
            paper = lesson.papers.filter(id=int(request.GET.get('paper_id')))
            if len(paper) > 0:
                paper = paper[0]
        if paper:
            paper_res = collect_paper(paper, profile)
        else:
            paper_res = []
        all_papers = []
        for paper in lesson.papers.all():
            all_papers.append([paper.id, paper.title])
        data = {
            'paper_res':paper_res,
            'title':lesson.title,
            'author_profile':lesson.author_profile.first_name,
            'author_profile_link':lesson.author_profile.get_absolute_url(),
            'done_by':len(lesson.done_by.all()),
            'try_by':len(lesson.try_by.all()),
            'all_papers':all_papers,
        }
        return JsonResponse(data)        
    else:
        return JsonResponse({})

def save_task(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('id'):
        if request.GET.get('id') == '-1':
            task = Task.objects.create()
            task.save()
            paper = school.school_papers.filter(id = int(request.GET.get('paper_id')))
            if len(paper) == 0:
                return JsonResponse({})
            paper = paper[0]
            subtheme = paper.subthemes.create()
            subtheme.task = task
            subtheme.save()
        else:
            task = Task.objects.filter(id=int(request.GET.get('id')))
            if len(task) == 0:
                return JsonResponse({})
            task = task[0]
        ans = request.GET.get('ans').split('@')
        print('xxxx', ans)
        variants = request.GET.get('variants').split('@')
        del ans[-1]
        del variants[-1]
        task.answer = ans
        task.text = request.GET.get('text')
        task.variants = variants
        if request.GET.get('type') == 'test':
            task.is_test = True
            task.is_mult_ans = False
        elif request.GET.get('type') == 'multans':
            task.is_test = False
            task.is_mult_ans = True
        else:
            task.is_test = False
            task.is_mult_ans = False
        task.save()
    data = {
    }
    return JsonResponse(data)

def delete_subtheme(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('id'):
        subtheme = Subtheme.objects.get(id=int(request.GET.get('id')))
        subtheme.delete()
    data = {
    }
    return JsonResponse(data)

def add_task_to_subtheme(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('id') and request.GET.get('paper_id'):
        task = Task.objects.filter(id=int(request.GET.get('id')))
        if len(task) == 0:
            return JsonResponse({})
        task = task[0]
        paper = school.school_papers.filter(id = int(request.GET.get('paper_id')))
        if len(paper) == 0:
            return JsonResponse({})
        paper = paper[0]
        subtheme = paper.subthemes.create()
        subtheme.task = task
        subtheme.save()
    data = {
    }
    return JsonResponse(data)

def get_all_tasks(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    school = is_moderator_school(request, profile)
    res = []
    tasks = Task.objects.all()
    for task in tasks:
        res.append(collect_task(task, False, profile))
    data = {
        "res":res,
    }
    return JsonResponse(data)

def save_paper_title(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('paper_id') and request.GET.get('title'):
        paper = school.school_papers.filter(id = int(request.GET.get('paper_id')))
        if len(paper) == 0:
            return JsonResponse({})
        paper = paper[0]
        paper.title = request.GET.get('title')
        paper.save()
    data = {
    }
    return JsonResponse(data)
