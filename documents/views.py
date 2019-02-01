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
from docs.models import Document
from docs.form import FileForm
from django.contrib.auth.models import User

def documents(request):
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    else:
        raise Http404

    file_form = FileForm(request.POST or None, request.FILES or None)
    if file_form.is_valid():
        doc = Document.objects.create(file = file_form.cleaned_data.get("file"))
        doc.save()
        return redirect('/documents')

    context = {
        "profile": profile,
        'yourid':profile.id,
        'root':True,
        'docfolders':DocumentFolder.objects.all(),
        'documents':Document.objects.all(),
        'cache':DocumentCache.objects.get_or_create(author_profile = profile)[0],
        'file_form':file_form,
    }
    return render(request, 'documents/documents.html', context)

def folders():
    folders = []
    for folder in DocumentFolder.objects.all():
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
    folder = DocumentFolder.objects.get(id=folder_id)

    file_form = FileForm(request.POST or None, request.FILES or None)
    if file_form.is_valid():
        doc = Document.objects.create(file = file_form.cleaned_data.get("file"))
        doc.save()
        folder.files.add(doc)
        return redirect(folder.get_absolute_url())

    context = {
        "profile": profile,
        'folder':folder,
        'cache':DocumentCache.objects.get_or_create(author_profile = profile)[0],
        'lessons':folder.files.all(),
        'folders':DocumentFolder.objects.filter(parent=folder),
        'tasks':Task.objects.all(),
        'file_form':file_form,
    }
    return render(request, 'documents/documents.html', context)

from django.http import JsonResponse
def file_action(request):
    profile = Profile.objects.get(user = request.user.id)
    cache = DocumentCache.objects.get_or_create(author_profile = profile)
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
    cache = DocumentCache.objects.get_or_create(author_profile = profile)
    cache = cache[0]
    title = ''
    if request.GET.get('new_parent') != 'library':
        new_parent = DocumentFolder.objects.get(id = int(request.GET.get('new_parent')))
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
    cache = DocumentCache.objects.get_or_create(author_profile = profile)
    cache = cache[0]
    title = ''
    link = ''
    title = copy_lesson(request)
    if request.GET.get('new_parent') != 'library':
        new_parent = DocumentFolder.objects.get(id = int(request.GET.get('new_parent')))
    if cache.object_type == 'folder':    
        folder = DocumentFolder.objects.get(id = cache.object_id)
        title = folder.title
        link = folder.get_absolute_url()

        if cache.action == 'copy':
            copy_folder = DocumentFolder.objects.create(author_profile = profile, title=folder.title)
            for child in folder.children.all():
                copy_child = DocumentFolder.objects.create(author_profile = profile, title=child.title)
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
                previous_parent = DocumentFolder.objects.get(id = cache.previous_parent)
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
    

def create_docfolder(request):
    profile = Profile.objects.get(user = request.user.id)
    if len(DocumentFolder.objects.all()) > 0:
        name = 'Новая папка' + str(DocumentFolder.objects.all()[len(DocumentFolder.objects.all())-1].id + 1)
    else:
        name = 'Новая папка'
    folder = DocumentFolder.objects.create(title = name)
    folder.author_profile = profile
    if request.GET.get('parent_id') != 'denone':
        parent = DocumentFolder.objects.get(id = int(request.GET.get('parent_id')))
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
            folder = DocumentFolder.objects.all()[len(DocumentFolder.objects.all())-1]
        else:
            folder = DocumentFolder.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('name'):
            folder.title = request.GET.get('name')
            folder.save()

    data = {}
    return JsonResponse(data)

def delete_folder(request):
    if request.GET.get('id'):
        folder = DocumentFolder.objects.get(id = int(request.GET.get('id')))
        folder.delete()
    data = {}
    return JsonResponse(data)
