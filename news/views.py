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
    title = request.GET.get('title')
    pid = request.GET.get('id')
    priority = int(request.GET.get('priority'))
    slug = request.GET.get('slug')
    post = save_post_work(title, pid, profile, school, priority, slug)
    data = {
        "url":post.get_edit_url(),
    }
    return JsonResponse(data)

def reorder_parts(post):
    i = 1
    for part in post.parts.all():
        part.order = i
        part.save()
        i+=1
def post_add_part(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    title = request.GET.get('title')
    pid = request.GET.get('post_id')
    priority = int(request.GET.get('priority'))
    slug = request.GET.get('slug')
    post = save_post_work(title, pid, profile, school, priority, slug)
    if slug == 'none7569wjd':
        slug = post.slug
    partid = int(request.GET.get('id'))
    file_url = ""
    file_name = ""
    url = post.get_edit_url()
    print('part', partid)
    if partid == -1:
        reorder_parts(post)
        part = post.parts.create(
            order=len(post.parts.all())+1,
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
            part.save()
            file_url = str(part.image.url)
        else:
            part.file = request.FILES.get('file')
            part.save()
            file_url = str(part.file.url)
    part.save()
    if request.GET.get('last') == 'yes':
        data = {
            "part_id":part.id,
            "file_url":file_url,
            "file_name":file_name,
            "url":url,
        }
    else:
        data = {
            "part_id":part.id,
            "slug":slug,
        }
    return JsonResponse(data)

def post_move_part(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    ok = False
    if request.GET.get('id') and request.GET.get('new_order'):
        move_part = PostPart.objects.get(id=int(request.GET.get('id')))
        post = move_part.post
        if school != post.school:
            return JsonResponse('Wrong')
        old_order = move_part.order
        new_order = int(request.GET.get('new_order'))
        move_part.order = new_order
        move_part.save()
        if old_order > new_order:
            qs = post.parts.filter(order__gte=new_order).exclude(id=move_part.id)
            for next_part in qs:
                new_order += 1
                next_part.order = new_order
                next_part.save()
        else:
            qs = post.parts.filter(order__lte=new_order).exclude(id=move_part.id)
            new_order = 0
            for next_part in qs:
                new_order += 1
                next_part.order = new_order
                next_part.save()
        ok = True
    data = {
        'ok':ok,
    }
    return JsonResponse(data)

def save_post_work(title, pid, profile, school, priority,slug):
    post_id = -1
    post = None
    if pid == '-1':
        found = False
        if slug != 'none7569wjd':
            find_by_slug = Post.objects.filter(slug=slug)
            if len(find_by_slug) > 0:
                post = find_by_slug[0]
                found = True
        if title and not found:
            slug = title.replace(' ', '_')
            last = len(Post.objects.filter(slug=slug))
            if last > 0:
                slug += str(last+1)
            post = school.school_posts.create(
                title = title,
                author_profile = profile,
                slug = slug,
                priority = priority,
                )
    else:
        post = school.school_posts.get(id=int(pid))
        post.title = title
        post.priority = priority
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
        posts = Post.objects.all().select_related('author_profile').select_related('school').prefetch_related('parts')
        page = int(request.GET.get('page'))
        p = Paginator(posts, 20)
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
                parts = post.parts.all()
                found_text = False
                found_img = False
                for part in parts:
                    if part.content != "" and found_text == False:
                        text = part.content[:70]
                        if len(text) >= 68:
                            text += '...'
                        found_text = True
                    if part.image and found_img == False:
                        found_img = True
                        print('found_img', post.title)
                        img = part.image.url
                    if found_text and found_img:
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

def post_new_comment(request):
    profile = get_profile(request)
    ok = False 
    if profile.image:
        avatar = profile.image.url
    else:
        avatar = 'images/nophoto.png'
    time = '' 
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
        ok = True
        time = comment.timestamp.strftime('%H:%M %d.%B.%Y')

    data = {
        "ok":ok,
        "author":profile.first_name,
        "author_url":profile.get_absolute_url(),
        'avatar':avatar,
        'time':avatar,
    }
    return JsonResponse(data)

def post_like_object(request):
    profile = get_profile(request)
    status = request.GET.get('status')
    if request.GET.get('id') and status:
        if request.GET.get('object') == 'comment':
            obj = Comment.objects.get(id=int(request.GET.get('id')))
        else:
            obj = Post.objects.get(id=int(request.GET.get('id')))
        if status == 'like':
            obj.likes.add(profile)
            obj.dislikes.remove(profile)
        elif status == 'nothing':
            obj.likes.remove(profile)
            obj.dislikes.remove(profile)
        elif status == 'dislike':
            obj.likes.remove(profile) 
            obj.dislikes.add(profile) 
    res = len(obj.likes.all()) - len(obj.dislikes.all())
    if res > 0:
        res = "+" + str(res)
    data = {
        "like_num":res,
    }
    return JsonResponse(data)

