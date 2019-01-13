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


def post_create(request):
    if not request.user.is_authenticated:
        raise Http404

    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    if not profile.is_trener:
        raise Http404
        
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())   
    
    context = {
        "form": form,
        "profile":profile,
    }
    return render(request, "news/post_create.html", context)

def post_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.height_field:
            instance.height_field = 0
        if not instance.width_field:
            instance.width_field = 0

        instance.save()
        return HttpResponseRedirect(instance.get_update_url())
        
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

    context = {
        "instance": instance,
        "form":form,
        "profile":profile,
    }
    return render(request, "news/post_create.html", context)

def post_list(request):
    if not request.user.is_authenticated:
        raise Http404
        
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "profile": profile,
        "posts":Post.objects.all(),
    }
    return render(request, "news/post_list.html", context)

def post_delete(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    try:
        instance = Post.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")
        
    if request.method == "POST":
        instance.delete()
        return redirect("posts:list")
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)

from django.http import JsonResponse


def change_curator(request):
    data = {
    }
    return JsonResponse(data)
