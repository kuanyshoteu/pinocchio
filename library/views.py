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

def library(request):
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    else:
        raise Http404

    context = {
        "profile": profile,
        'yourid':profile.id,
        'root':True,
        'folders':Folder.objects.all(),
        'lessons':Lesson.objects.all(),
        'cache':Cache.objects.get_or_create(author_profile = profile)[0],
        'tasks':Task.objects.all(),
    }
    return render(request, template_name='library.html', context=context)

def courses(request):
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "profile": profile,
        'yourid':profile.id,
        'folders':Folder.objects.all(),
        'courses':Course.objects.all(),
        'cache':Cache.objects.get_or_create(author_profile = profile)[0],
        'tasks':Task.objects.all(),
    }
    return render(request, 'courses/course_list.html', context=context)

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
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    else:
        raise Http404
    folder = Folder.objects.get(id=folder_id)

    context = {
        "profile": profile,
        'folder':folder,
        'cache':Cache.objects.get_or_create(author_profile = profile)[0],
        'lessons':folder.lesson_list.all(),
        'folders':Folder.objects.filter(parent=folder),
        'tasks':Task.objects.all(),
    }
    return render(request, template_name='library.html', context=context)

from django.http import JsonResponse
def file_action(request):
    profile = Profile.objects.get(user = request.user.id)
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

def copy_lesson(request):
    profile = Profile.objects.get(user = request.user.id)
    cache = Cache.objects.get_or_create(author_profile = profile)
    cache = cache[0]
    title = ''
    if request.GET.get('new_parent') != 'library':
        new_parent = Folder.objects.get(id = int(request.GET.get('new_parent')))
    if cache.object_type == 'lesson':
        lesson = Lesson.objects.get(id = cache.object_id)
        new_lesson = Lesson.objects.create(user=request.user, author_profile = profile, title = lesson.title, content = lesson.content)
        
        for task in lesson.task_list.all():
            new_task = Task.objects.create(user=request.user, 
                author_profile = profile, text = task.text, answer = task.answer, 
                height_field = task.height_field, width_field = task.width_field)
            if task.image:
                new_task.image = task.image
            new_task.save()
            new_lesson.task_list.add(new_task)

        if request.GET.get('new_parent') != 'library':
            new_parent.lesson_list.add(lesson)
        if cache.action == 'cut':
            lesson.delete()
    return title

def paste(request):
    profile = Profile.objects.get(user = request.user.id)
    cache = Cache.objects.get_or_create(author_profile = profile)
    cache = cache[0]
    title = ''
    link = ''
    title = copy_lesson(request)
    if request.GET.get('new_parent') != 'library':
        new_parent = Folder.objects.get(id = int(request.GET.get('new_parent')))
    if cache.object_type == 'folder':    
        folder = Folder.objects.get(id = cache.object_id)
        title = folder.title
        link = folder.get_absolute_url()

        if cache.action == 'copy':
            copy_folder = Folder.objects.create(author_profile = profile, title=folder.title)
            for child in folder.children.all():
                copy_child = Folder.objects.create(author_profile = profile, title=child.title)
                copy_folder.children.add(copy_child)
            for ppr in folder.lesson_list.all():
                copy_folder.lesson_list.add(ppr)

            copy_folder.parent = new_parent
            new_parent.children.add(copy_folder)
            copy_folder.save()

        elif cache.action == 'cut':
            folder.parent = new_parent
            new_parent.children.add(folder)
            folder.save()
            if cache.previous_parent > 0:
                previous_parent = Folder.objects.get(id = cache.previous_parent)
                previous_parent.children.remove(folder)
    else:
        lesson = Lesson.objects.get(id = cache.object_id)
        title = lesson.title
        link = lesson.get_absolute_url()

        new_parent.lesson_list.add(lesson)
        lesson.save()
        if cache.action == 'cut' and cache.previous_parent > 0:
            previous_parent = Lesson.objects.get(id = cache.previous_parent)
            previous_parent.lesson_list.remove(lesson)
                
    data = {
        'status':'ok',
        'object_type':cache.object_type,
        'title':title,
        'link':link,
    }
    return JsonResponse(data)
    

def create_folder(request):
    profile = Profile.objects.get(user = request.user.id)
    if len(Folder.objects.all()) > 0:
        name = 'Новая папка' + str(Folder.objects.all()[len(Folder.objects.all())-1].id + 1)
    else:
        name = 'Новая папка'
    folder = Folder.objects.create(title = name)
    folder.author_profile = profile
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
    if request.GET.get('id'):
        folder = Folder.objects.get(id = int(request.GET.get('id')))
        folder.delete()
    data = {}
    return JsonResponse(data)
