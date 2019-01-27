from django.shortcuts import render, redirect
from accounts.models import *
from .models import *
from accounts.forms import *
from squads.models import Squad

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from itertools import chain
from django.views.generic import ListView

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.contrib.auth.models import User
def loaderio(request):
    context = {
    }
    return render(request, "loaderio.txt", context)

def main_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        return redirect(profile.get_absolute_url())    

    form = EmptyForm(request.POST or None)
    if form.is_valid():
        if request.POST.get('username') and request.POST.get('password'):
            for profile in Profile.objects.all():
                if profile.mail == request.POST.get('username') or profile.phone == request.POST.get('username'):
                    user = authenticate(username=str(profile.user.username), password=str(request.POST.get('password')))
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(profile.get_absolute_url())

    context = {
        'main':True,
        'form':form,
    }
    return render(request, "main.html", context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def login_view(request):
    if request.GET.get('username') and request.GET.get('password'):
        for profile in Profile.objects.all():
            if profile.mail == request.GET.get('username') or profile.phone == request.GET.get('username'):
                print(request.GET.get('password'),profile.user.username)
                user = authenticate(username=str(profile.user.username), password=str(request.GET.get('password')))
                login(request, user)
                break
    data = {
    }
    return JsonResponse(data)

def register_view(request):
    if request.GET.get('first_name') and request.GET.get('second_name') and request.GET.get('school') and request.GET.get('phone') and request.GET.get('mail') and request.GET.get('password1') and request.GET.get('password2'):
        if request.GET.get('password1') == request.GET.get('password2'):
            new_id = User.objects.order_by("id").last().id + 1
            user = User.objects.create(username='user' + str(new_id), password=request.GET.get('password1'))
            new_user = authenticate(username = user.username, password=request.GET.get('password1'))
            login(request, user)
            profile = Profile.objects.get(user = user)
            profile.first_name = request.GET.get('first_name')
            profile.second_name = request.GET.get('second_name')
            profile.school = request.GET.get('school')
            profile.phone = request.GET.get('phone')
            profile.mail = request.GET.get('mail')
            profile.save()
    data = {
    }
    return JsonResponse(data)

def ChangeSubject(request):
    if request.GET.get('id'):
        subject = Subject.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('text'):
            subject.text = request.GET.get('text')
        if request.GET.get('title'):
            subject.title = request.GET.get('title')
        if request.GET.get('cost'):
            subject.cost = request.GET.get('cost')
        subject.save()
                    
    data = {
        "like_num":0,
    }
    return JsonResponse(data)

def SaveZaiavka(request):
    if request.GET.get('name'):
        if request.GET.get('phone'):
            zaiavka = Zaiavka.objects.create(name=request.GET.get('name'), phone=request.GET.get('phone'))
    data = {
    }
    return JsonResponse(data)


class CityAPIToggle(APIView):
    def get(self, request, format=None):
        #print("dedede")
        data = {
            "like_num":0,
        }
        return Response(data)

class FilialAPIToggle(APIView):
    def get(self, request, format=None):
        data = {
            "like_num":0,
        }
        return Response(data)

class SubjectAPIToggle(APIView):
    def get(self, request, format=None):
        #print("dedede")
        data = {
            "like_num":0,
        }
        return Response(data)

def contacts_view(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "profile":profile,
    }
    return render(request, "contacts.html", context)


def trener_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Trener, slug=slug)
    form = TrenerForm(request.POST or None, request.FILES or None, instance=instance)
    main_page = 'de'
    if len(MainPage.objects.all()) < 1:
        main_page = MainPage.objects.create()
    else:
        main_page = MainPage.objects.all()[0]
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(main_page.main_url())
    
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
        "user":request.user,
        "profile":profile,
    }
    return HttpResponseRedirect(main_page.main_url())



def trener_delete(request, slug=None):
    try:
        instance = Trener.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        reponse.status_code = 403 
        return HttpResponse("You do not have permission to do this.")

    main_page = 'de'
    if len(MainPage.objects.all()) < 1:
        main_page = MainPage.objects.create()
    else:
        main_page = MainPage.objects.all()[0]
    if request.method == "POST":
        instance.delete()
        return HttpResponseRedirect(main_page.main_url())
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)
