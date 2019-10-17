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
from schools.models import School
from papers.models import *
from .models import *
from todolist.models import Document
from todolist.form import FileForm
from django.contrib.auth.models import User
from constants import *

def documents(request):
    profile = get_profile(request)    
    only_staff(profile)
    school = profile.schools.first()
    return redirect(school.get_school_documents())

def school_documents(request, school_id):
    profile = get_profile(request)
    only_staff(profile)
    school = School.objects.get(id=school_id)
    is_in_school(profile, school)
    img = ['png', 'jpg', 'jpeg']
    html = ['html', 'css', 'js', 'py', 'java']
    file_form = FileForm(request.POST or None, request.FILES or None)
    if file_form.is_valid():
        doc = Document.objects.create(file = file_form.cleaned_data.get("file"))
        print(doc)
        file = str(file_form.cleaned_data.get("file"))

        if file.split('.')[-1] in img:
            doc.object_type = 'img'
        elif file.split('.')[-1] == 'pdf':
            doc.object_type = 'pdf'
        elif file.split('.')[-1] == 'xls':
            doc.object_type = 'xls'
        elif file.split('.')[-1] == 'doc':
            doc.object_type = 'doc'
        elif file.split('.')[-1] == 'txt':
            doc.object_type = 'txt'
        elif file.split('.')[-1] == 'mp3':
            doc.object_type = 'mp3'
        elif file.split('.')[-1] == 'ppt':
            doc.object_type = 'ppt'
        elif file.split('.')[-1] in html:
            doc.object_type = 'html'
        doc.school = school
        doc.save()
        return redirect('/documents')
    print('******************** docs')
    context = {
        "profile": profile,
        'yourid':profile.id,
        'root':True,
        "docs":school.school_docs.all(),
        "docfolders":school.school_docfolders.all(),
        'hisschools':profile.schools.all(),
        "current_school_id":school.id,
        'cache':DocumentCache.objects.get_or_create(author_profile = profile)[0],
        'file_form':file_form,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":school.money,
    }
    return render(request, 'documents/documents.html', context)

def folder_details(request, folder_id=None):
    profile = get_profile(request)
    only_staff(profile)
    folder = DocumentFolder.objects.get(id=folder_id)
    school = folder.school
    is_in_school(profile, school)    
    file_form = FileForm(request.POST or None, request.FILES or None)
    if file_form.is_valid():
        doc = Document.objects.create(file = file_form.cleaned_data.get("file"))
        doc.save()
        folder.files.add(doc)
        return redirect(folder.get_absolute_url())

    context = {
        "profile": profile,
        'this_folder':folder,
        'docs_from_schools':[folder.title],
        'cache':DocumentCache.objects.get_or_create(author_profile = profile)[0],
        'folders':DocumentFolder.objects.filter(parent=folder),
        'file_form':file_form,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),  
        "school_money":profile.schools.first().money,      
    }
    return render(request, 'documents/documents.html', context)

from django.http import JsonResponse
def file_action(request):
    profile = Profile.objects.get(user = request.user.id)
    only_staff(profile)
    cache = DocumentCache.objects.get_or_create(author_profile = profile)
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
    only_staff(profile)
    cache = DocumentCache.objects.get_or_create(author_profile = profile)[0]
    title = ''
    link = ''
    if request.GET.get('new_parent') != 'root':
        new_parent = DocumentFolder.objects.get(id = int(request.GET.get('new_parent')))
        school = new_parent.school
    elif request.GET.get('school_id'):
        school = School.objects.get(id=int(request.GET.get('school_id')))
    is_in_school(profile, school)
    if cache.object_type == 'folder':    
        folder = DocumentFolder.objects.get(id = cache.object_id)
        title = folder.title
        link = folder.get_absolute_url()
        copy_folder = DocumentFolder.objects.create(author_profile = profile, title=folder.title, school=folder.school)
        for doc in folder.files.all():
            copy_folder.files.add(doc)
        if request.GET.get('new_parent') != 'root':
            copy_folder.parent = new_parent
            new_parent.children.add(copy_folder)
        elif request.GET.get('school_id'):
            copy_folder.school = school
        copy_folder.save()
        if cache.action == 'cut' and cache.previous_parent > 0:
            folder.delete()
    else:
        doc = Document.objects.get(id = cache.object_id)
        new_doc = Document.objects.create(file = doc.file, object_type = doc.object_type, school=doc.school)
        link = new_doc.file.url
        if request.GET.get('new_parent') != 'root':
            new_parent.files.add(new_doc)
        elif request.GET.get('school_id'):
            new_doc.school = school
        new_doc.save()
        if cache.action == 'cut' and cache.previous_parent > 0:
            doc.delete()
            cache.action='copy'
            cache.object_id = new_doc.id
            cache.save()
    data = {
        'status':'ok',
        'object_type':cache.object_type,
        'link':link,
    }
    return JsonResponse(data)
    

def create_docfolder(request):
    profile = Profile.objects.get(user = request.user.id)
    only_staff(profile)
    print('***********')
    if request.GET.get('school_id'):
        school = School.objects.get(id=int(request.GET.get('school_id')))
        is_in_school(profile, school)
        if len(school.school_docfolders.all()) > 0:
            name = 'Папка' + str(school.school_docfolders.all()[len(school.school_docfolders.all())-1].id + 1)
        else:
            name = 'Папка'
        folder = DocumentFolder.objects.create(title = name)
        folder.author_profile = profile
        if request.GET.get('school_id'):
            folder.school = school
        if request.GET.get('parent_id') != 'none':
            parent = DocumentFolder.objects.get(id = int(request.GET.get('parent_id')))
            folder.parent = parent
            parent.children.add(folder)
        folder.save()
    data = {
        'name':name,
        'url':folder.get_absolute_url(),
    }
    return JsonResponse(data)

def change_docname(request):
    profile = Profile.objects.get(user = request.user.id)
    only_staff(profile)
    if request.GET.get('id'):
        if request.GET.get('id') == 'new':
            folder = DocumentFolder.objects.all()[len(DocumentFolder.objects.all())-1]
        else:
            folder = DocumentFolder.objects.get(id = int(request.GET.get('id')))
        school = folder.school
        is_in_school(profile, school)
        if request.GET.get('name'):
            folder.title = request.GET.get('name')
            folder.save()

    data = {}
    return JsonResponse(data)

def delete_folder(request):
    profile = Profile.objects.get(user = request.user.id)
    only_staff(profile)
    deleted = False
    if request.GET.get('id'):
        folder = DocumentFolder.objects.get(id = int(request.GET.get('id')))
        school = folder.school
        is_in_school(profile, school)
        if folder.author_profile == profile:
            folder.delete()
            deleted = True
    data = {
        'deleted':deleted,
    }
    return JsonResponse(data)

def delete_document(request):
    profile = Profile.objects.get(user = request.user.id)
    only_staff(profile)
    if request.GET.get('id'):
        doc = Document.objects.get(id = int(request.GET.get('id')))
        school = doc.school
        is_in_school(profile, school)
        doc.delete()
    data = {}
    return JsonResponse(data)
