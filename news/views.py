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

def blog(request):
    schools = []
    if request.user.is_authenticated:
        profile = get_profile(request)
        is_moderator = is_profi(profile, 'Moderator')
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
        is_moderator = is_profi(profile, 'Moderator')        
        profile = get_profile(request)
        school = is_moderator_school(request, profile)
        schools.append(school)
    else:
        profile = False    
        is_moderator = False
        is_trener = False
        is_manager = False
        is_director = False
        is_moderator = False   

    bilimtap = School.objects.get(title='Штаб квартира ЦРУ')
    schools.append(bilimtap)
    posts = Post.objects.all().select_related('author_profile').select_related('school').prefetch_related('parts')
    p = Paginator(posts, 20)
    page1 = p.page(1)

    context = {
        "profile":profile,
        "schools":School.objects.all(),
        "professions":Profession.objects.all(),
        "is_moderator":is_moderator,
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director,
        "is_moderator":is_moderator,
        "posts":page1.object_list,
    }
    return render(request, "blog.html", context)

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
    school = False
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

def post_delete(request, slug):
    profile = Profile.objects.get(user = request.user)
    post = Post.objects.get(slug = slug)
    if post.author_profile == profile:
        post.delete()
        return redirect("main:blog")
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

def save_post(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    pid = request.GET.get('id')
    post = save_post_work(pid, profile, school)
    oldslug = post.slug
    if request.GET.get('is_images') == '0':
        text = request.GET.get('text')
        is_first = request.GET.get('first')
        if is_first == 'yes':
            title = request.GET.get('title')
            post.title = title
            post.slug = create_slug(title)
            post.text = text
        else:
            post.text += text
    else:
        post.priority = int(request.GET.get('priority'))
        old_files = request.GET.get('old_files').split(',')
        for part in post.parts.all():
            if str(part.id) in old_files:
                part.order = 0
                part.save()
            else:
                part.delete()
        for file in request.FILES:
            print('file', file)
            part = post.parts.create()
            part.image = request.FILES.get(file)
            part.save()
            print('new_file_place'+file)
            print(post.text)
            post.text = post.text.replace('new_file_place'+file, '<img class="post_file" src="'+part.image.url+'">')
            print('after replace', post.text)
    post.save()
    newslug = post.slug
    if request.GET.get('last') == 'yes':
        if newslug != oldslug:
            update = True
        else:
            update = False
        data = {
            "url":post.get_edit_url(),
            'update':update,    
        }
    elif request.GET.get('is_images') == '1':
        data = {'id':post.id}
    else:
        data = {}
    return JsonResponse(data)

def create_slug(title):
    slug = slugify(translit(title[:45], 'ru', reversed=True))
    last = len(Post.objects.filter(slug=slug))
    if last > 1:
        slug += str(last+1)
    return slug

def save_post_work(pid, profile, school):
    if pid == '-1':
        post = school.school_posts.create(
            title = title,
            author_profile = profile,
            )
    else:
        post = school.school_posts.get(id=int(pid))
    return post

def get_posts(request):
    print('get_posts')
    res = []
    print('page', request.GET.get('page'))
    if request.GET.get('page'):
        schools = []
        if request.user.is_authenticated:
            profile = get_profile(request)
            school = is_moderator_school(request, profile)
            schools.append(school)
        bilimtap = School.objects.get(title='Штаб квартира ЦРУ')
        schools.append(bilimtap)
        posts = Post.objects.all().select_related('author_profile').select_related('school').prefetch_related('parts')
        page = int(request.GET.get('page'))
        p = Paginator(posts, 20)
        page1 = p.page(page)
        for post in page1.object_list:
            limit = 70*post.priority
            text = post.text[:limit]
            if len(text) >= limit - 2:
                text += '...'                
            img = ""
            file = ""
            author = ""
            author_url = ""
            school_title = ""
            school_url = ""
            if len(post.parts.all()) > 0:
                parts = post.parts.all()
                found_img = False
                for part in parts:
                    if part.image and found_img == False:
                        found_img = True
                        img = part.image.url
                    if found_img:
                        break
            res.append([
                post.title,                 #0
                text,                       #1
                img,                        #2
                post.get_absolute_url(),    #3
                file,                       #4
                post.priority,              #9
                ])
    data = {
        "posts":res,
    }
    return JsonResponse(data)

def post_new_comment(request):
    profile = get_profile(request)
    ok = False 
    if profile.image:
        avatar = profile.image.url
    else:
        avatar = 'images/nophoto.png'
    time = '' 
    cid = -1
    comment_id = int(request.GET.get('comment_id'))
    if request.GET.get('post_id') and request.GET.get('content') and comment_id:
        post = Post.objects.get(id=int(request.GET.get('post_id')))
        if comment_id > 0:
            comment = post.comments.filter(id=int(comment_id))
            if len(comment) > 0:
                comment = comment[0]
        else:
            comment = post.comments.create(
                author_profile = profile,
                )
        parent_id = int(request.GET.get('parent_id'))
        if parent_id > 0:
            parent = post.comments.filter(id=parent_id)
            if len(parent) > 0:
                parent = parent[0]
                comment.parent = parent
                comment.level = parent.level + 1
        comment.content = request.GET.get('content')
        comment.save()
        cid = comment.id
        ok = True
        time = comment.timestamp.strftime('%H:%M %d %B %Y')
    data = {
        "ok":ok,
        "author":profile.first_name,
        "author_url":profile.get_absolute_url(),
        'avatar':avatar,
        'time':time,
        'id':cid,
    }
    return JsonResponse(data)

def post_like_object(request):
    profile = get_profile(request)
    status = request.GET.get('status')
    object_name = request.GET.get('object')
    if request.GET.get('id') and status:
        new_status = 'none'
        if object_name == 'comment':
            obj = Comment.objects.get(id=int(request.GET.get('id')))
        else:
            obj = Post.objects.get(id=int(request.GET.get('id')))
        if status == 'like':
            if profile in obj.likes.all():
                obj.likes.remove(profile)
            else:
                obj.likes.add(profile)
                new_status = 'like'
            obj.dislikes.remove(profile)
        elif status == 'none':
            obj.likes.remove(profile)
            obj.dislikes.remove(profile)
        elif status == 'dislike':
            if profile in obj.dislikes.all():
                obj.dislikes.remove(profile) 
            else:
                obj.dislikes.add(profile) 
                new_status = 'dislike'
            obj.likes.remove(profile) 
    res = len(obj.likes.all()) - len(obj.dislikes.all())
    if res > 0:
        res = "+" + str(res)
    data = {
        "like_num":res,
        "status":new_status,
    }
    return JsonResponse(data)

def get_post(request):
    res = []
    if request.GET.get('id'):
        post = Post.objects.get(id=int(request.GET.get('id')))
        for part in post.parts.all():
            if part.image:
                res.append([part.image.url, part.id, part.order])
    data = {
        "content":post.text,
        "images":res,
    }
    return JsonResponse(data)

def get_comments(request):
    res = []
    if request.GET.get('post_id') and request.GET.get('page'):
        post = Post.objects.get(id=int(request.GET.get('post_id')))
        p = Paginator(post.comments.filter(level=1).select_related('parent').prefetch_related('likes').prefetch_related('dislikes'), 20)
        page1 = p.page(int(request.GET.get('page')))
        if request.user.is_authenticated:
            profile = get_profile(request)
        for comment in page1.object_list:
            author = comment.author_profile
            name = author.first_name
            url = author.get_absolute_url()
            parent_id = ''
            if comment.parent:
                parent_id = comment.parent.id
            if author.image:
                img = author.image.url
            else:
                img = "images/nophoto.png"
            if author in comment.likes.all():
                like_status = 'like'
            elif author in comment.dislikes.all():
                like_status = 'dislike'
            else:
                like_status = 'none'
            res.append([
                name,
                url,
                img,
                comment.timestamp.strftime('%H:%M %d %B %Y'),
                comment.content,
                comment.id,
                parent_id,
                len(comment.likes.all()) - len(comment.dislikes.all()),
                like_status,
                ])
    data = {
        "comments":res,
    }
    return JsonResponse(data)