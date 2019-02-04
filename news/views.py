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

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    profile = ''
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "instance": instance,
        "profile":profile,
    }
    return render(request, "news/post_detail.html", context)


def post_list(request):
    if not request.user.is_authenticated:
        raise Http404
        
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    if request.POST: 
        text = request.POST.get('post_text')
        newpost = Post.objects.create(author_profile=profile,content=text)
        if len(request.FILES) > 0:
            print('f', request.FILES)
            file = request.FILES['postfile']
            newpost.image = file
            newpost.save()
        return HttpResponseRedirect('/news')
    
    context = {
        "profile": profile,
        "posts":Post.objects.all(),
    }
    return render(request, "news/post_list.html", context)

def post_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    if profile.is_manager:
        post = Post.objects.get(id=int(request.GET.get('post_id')))
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
