from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView
from datetime import timedelta
from .forms import PostForm
from .models import *
from accounts.models import Profile
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User
from django.template import RequestContext
from constants import *
from django.http import JsonResponse

def post_list(request, school_id):
    profile = ''
    hisschools = []
    is_trener = False
    is_director = False
    is_manager = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
        hisschools = profile.schools.all()
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
    school = is_moderator_school(request, profile)
    context = {
        "profile": profile,
        "posts": school.school_posts.all(),
        'hisschools':hisschools,
        "current_school_id":school.id,
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
        "school_money":school.money,
        "page":"news",
        "school_crnt":school,
    }
    return render(request, "news/post_list.html", context)

def post_detail(request, slug):
    profile = ''
    hisschools = []
    is_trener = False
    is_director = False
    is_manager = False
    school_money = 0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
        school = is_moderator_school(request, profile)
        school_money = school.money
    post = Post.objects.get(slug = slug)
    context = {
        "profile": profile,
        "post":post,
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
        "school_money":school_money,
        "page":"news",
        "school_crnt":school,
    }
    return render(request, "news/post_detail.html", context)

def new_post(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    context = {
        "profile": profile,
        "current_school_id":school.id,
        "post":False,
        "school_money":school.money,
        "page":"news",
        "school_crnt":school,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
    }
    return render(request, "news/new_post.html", context)

def post_edit(request, slug):
    profile = get_profile(request)
    school = is_moderator_school(request, profile)
    post = Post.objects.get(slug = slug)
    context = {
        "profile": profile,
        "post":post,
        "current_school_id":school.id,
        "school_money":school.money,
        "page":"news",
        "school_crnt":school,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
    }
    return render(request, "news/new_post.html", context)

def post_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    if is_profi(profile, 'Manager'):
        post = Post.objects.get(id=int(request.GET.get('post_id')))
        is_in_school(profile, post.school)       
        post.delete()
    data = {
    }
    return JsonResponse(data)

def save_post(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    title = request.GET.get('title')
    pid = request.GET.get('id')
    post = save_post_work(title, pid, profile, school)
    data = {
        "url":post.get_edit_url(),
    }
    return JsonResponse(data)

def post_add_part(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    title = request.GET.get('title')
    pid = request.GET.get('post_id')
    post = save_post_work(title, pid, profile, school)
    partid = int(request.GET.get('id'))
    img = ""
    file_name = ""
    url = post.get_edit_url()
    print('part', partid)
    if partid == -1:
        part = post.parts.create(
            order=len(post.parts.all()),
        )
    else:
        part = post.parts.get(id=partid)
    if request.GET.get('first') == 'yes':
        part.content = request.GET.get('text')
    else:
        part.content += request.GET.get('text')
    if request.FILES.get('file'):
        file_name = str(request.FILES.get('file'))
        its_img = False
        for frmt in img_formats:
            if frmt in file_name:
                its_img = True
                break
        if its_img:
            part.image = request.FILES.get('file')
            img = str(part.image.url)
        else:
            part.file = request.FILES.get('file')
    part.save()
    if request.GET.get('last') == 'yes':
        data = {
            "part_id":part.id,
            "img":img,
            "file_name":file_name,
            "url":url,
        }
    else:
        data = {
            "part_id":part.id,
        }
    return JsonResponse(data)

def save_post_work(title, pid, profile, school):
    post_id = -1
    post = None
    if pid == '-1':
        if title:
            slug = title.replace(' ', '_')
            last = len(Post.objects.filter(slug=slug))
            if last > 0:
                slug += str(last+1)
            post = school.school_posts.create(
                title = title,
                author_profile = profile,
                slug = slug,
                )
    else:
        post = school.school_posts.get(id=int(pid))
        post.title = title
        post.save()
    return post

def get_posts(request):
    res = []
    if request.GET.get('page'):
        schools = []
        if request.user.is_authenticated:
            profile = get_profile(request)
            school = is_moderator_school(request, profile)
            schools.append(school)
        bilimtap = School.objects.get(title='Штаб квартира ЦРУ')
        schools.append(bilimtap)
        posts = Post.objects.filter(school__in=[school, bilimtap])
        page = int(request.GET.get('page'))
        p = Paginator(posts, 5)
        page1 = p.page(page)
        for post in page1.object_list:
            text = ""
            img = ""
            file = ""
            author = ""
            author_url = ""
            school_title = ""
            school_url = ""
            if len(post.parts.all()) > 0:
                parts = post.parts.filter(show=True)
                for part in parts:
                    if part.content != "":
                        text = part.content
                    elif part.image:
                        img = part.image.url
                    elif part.file:
                        file = part.file.url
            if post.author_profile:
                author = post.author_profile.first_name
                author_url = post.author_profile.get_absolute_url()
            if post.school:
                school_title = post.school.title
                school_url = post.school.landing()
            res.append([
                post.title,                 #0
                text,                       #1
                img,                        #2
                post.get_absolute_url(),    #3
                file,                       #4
                author,                     #5
                author_url,                 #6
                school_title,               #7
                school_url,                 #8
                post.priority,              #9
                ])
    data = {
        "posts":res,
    }
    return JsonResponse(data)

def post_delete_part(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)  
    ok = False  
    if request.GET.get('id'):
        part = PostPart.objects.get(id=int(request.GET.get('id')))
        post = part.post
        pschool = post.school
        if pschool == school:
            part.delete()
            ok = True
    data = {
        "ok":ok,
    }
    return JsonResponse(data)
