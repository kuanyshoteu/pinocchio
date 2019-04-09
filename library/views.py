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
    only_teachers(profile)
    school = profile.schools.first()
    return redirect(school.get_school_library())

def school_library(request, school_id):
    profile = get_profile(request)
    only_teachers(profile)
    school = School.objects.get(id=school_id)
    context = {
        "profile": profile,
        'yourid':profile.id,
        'root':True,
        "lessons":school.lessons.all(),
        "folders":school.school_folders.all(),
        'hisschools':profile.schools.all(),
        "current_school_id":school.id,
        'cache':Cache.objects.get_or_create(author_profile = profile)[0],
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),   
    }
    return render(request, 'library/library.html', context=context)

def folders():
    folders = []
    for folder in Folder.objects.all():
        if not folder.parent:
            folders.append(folder)
    return (folders)

def lessons_array():
    lessons = []
    for lesson in Lesson.objects.all():
        if len(lesson.folder.all()) == 0:
            lessons.append(lesson)
    return (lessons)

def folder_details(request, folder_id=None):
    profile = get_profile(request)
    only_teachers(profile)
    folder = Folder.objects.get(id=folder_id)
    context = {
        "profile": profile,
        'folder':folder,
        'cache':Cache.objects.get_or_create(author_profile = profile)[0],
        'lessons':folder.lesson_list.all(),
        'folders':folder.children.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'), 
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
    print(cache.object_id)
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
    elif request.GET.get('school_id'):
        school = School.objects.get(id=int(request.GET.get('school_id')))
    if cache.object_type == 'folder':    
        folder = Folder.objects.get(id = cache.object_id)
        title = folder.title
        link = folder.get_absolute_url()
        copy_folder = Folder.objects.create(author_profile = profile, title=folder.title)
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
        new_lesson = Lesson.objects.create(author_profile = profile, title = lesson.title)
        new_lesson.save()
        title = new_lesson.title
        link = new_lesson.get_absolute_url()
        for paper in lesson.papers.all():
            new_paper = Paper.objects.create(title=paper.title,
                author_profile=paper.author_profile,typee=paper.typee)
            for subtheme in paper.subthemes.all():
                new_subtheme = Subtheme.objects.create(content=subtheme.content,video=subtheme.video,
                    youtube_video_link=subtheme.youtube_video_link)
                new_paper.subthemes.add(new_subtheme)
                for task in subtheme.task_list.all():
                    new_task = Task.objects.create(
                        author_profile = profile, text = task.text, answer = task.answer, 
                        height_field = task.height_field, width_field = task.width_field)
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
    if request.GET.get('school_id'):
        school = School.objects.get(id=int(request.GET.get('school_id')))
    if len(school.school_folders.all()) > 0:
        name = 'Папка' + str(school.school_folders.all()[len(school.school_folders.all())-1].id + 1)
    else:
        name = 'Папка'
    folder = Folder.objects.create(title = name)
    folder.author_profile = profile
    if request.GET.get('school_id'):
        folder.school = school
    if request.GET.get('parent_id') != 'denone':
        parent = Folder.objects.get(id = int(request.GET.get('parent_id')))
        folder.parent = parent
        parent.children.add(folder)
    folder.save()
    data = {
        'name':name,
        'url':folder.get_absolute_url(),
    }
    return JsonResponse(data)

def change_name(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        if request.GET.get('id') == 'new':
            folder = Folder.objects.all()[len(Folder.objects.all())-1]
        else:
            folder = Folder.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('name'):
            folder.title = request.GET.get('name')
            folder.save()

    data = {}
    return JsonResponse(data)

def delete_folder(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        folder = Folder.objects.get(id = int(request.GET.get('id')))
        folder.delete()
    data = {}
    return JsonResponse(data)
