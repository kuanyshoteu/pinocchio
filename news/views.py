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

def news(request):
    profile = get_profile(request)
    if len(profile.schools.all()) == 0:
        context = {
            "profile": profile,
            "posts": [],
            'hisschools':[],
            "current_school_id":0,
            'is_trener':is_profi(profile, 'Teacher'),
            "is_manager":is_profi(profile, 'Manager'),
            "is_director":is_profi(profile, 'Director'), 
            "page":"news",
        }
        return render(request, "news/post_list.html", context)        
    else:
        school = profile.schools.first()
        return redirect(school.get_school_posts())

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
    school = School.objects.get(id=school_id)
    if request.POST: 
        text = request.POST.get('post_text')
        newpost = Post.objects.create(author_profile=profile,content=text, school=school)
        if len(request.FILES) > 0:
            file = request.FILES['postfile']
            newpost.image = file
            newpost.save()
        return redirect(school.get_school_posts())
    
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
    }
    return render(request, "news/post_list.html", context)

def post_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    if is_profi(profile, 'Manager'):
        post = Post.objects.get(id=int(request.GET.get('post_id')))
        is_in_school(profile, post.school)       
        post.delete()
    data = {
    }
    return JsonResponse(data)

from django.http import JsonResponse


def create_post(request):
    profile = Profile.objects.get(user = request.user.id)
    data = {
    }
    return JsonResponse(data)
