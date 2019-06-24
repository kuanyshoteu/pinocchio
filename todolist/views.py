import json

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage

from .models import *
from accounts.models import *
from .form import *
from constants import *

@ensure_csrf_cookie
def index(request):
    profile = get_profile(request)
    only_staff(profile)
    school = profile.schools.first()
    return render(request, template_name='kanban/base.html', context={
        'boards': school.school_boards.all(),
        "profile":profile,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        'hint':profile.skill.hint_numbers[6],
    })

def new_board(request):
    profile = get_profile(request)
    only_staff(profile)
    school = profile.schools.first()
    name = request.POST.get('board_name')
    assert name
    Board.objects.create(name=name, school=school)
    return redirect('/todolist')

def new_column(request):
    profile = get_profile(request)
    only_staff(profile)
    if request.POST.get('board_id'):
        board_id = int(request.POST.get('board_id'))
    title = request.POST.get('column_title')
    if title: 
        Column.objects.create(title=title, board_id=board_id)
    return redirect('/todolist')

def new_card(request):
    profile = get_profile(request)
    only_staff(profile)
    column_id = int(request.POST.get('column_id'))
    title = request.POST.get('title')
    assert title and column_id
    Card.objects.create(title=title, column_id=column_id)
    return redirect('/todolist')

def view_card(request, card_id, card_slug):
    profile = get_profile(request)
    only_staff(profile)
    school = profile.schools.first()

    card = Card.objects.get(id=int(card_id))
    file_form = FileForm(request.POST or None, request.FILES or None)
    if file_form.is_valid():
        doc = Document.objects.create(file = file_form.cleaned_data.get("file"))
        doc.save()
        card.doc_list.add(doc)
        card.save()
        return redirect(card.get_absolute_url())

    comment_form = CommentForm(request.POST or None, request.FILES or None)
    if comment_form.is_valid():
        comment = Comment.objects.create(
                author_profile = profile,
                card = card,
                content = comment_form.cleaned_data.get('content'),
            )
        if comment_form.cleaned_data.get("image"):
            comment.image = comment_form.cleaned_data.get("image")
        if comment_form.cleaned_data.get("ffile"):
            doc = Document.objects.create(file = comment_form.cleaned_data.get("ffile"))
            doc.save()
            comment.ffile.add(doc)
        comment.save()
        return redirect(card.get_absolute_url())

    return render(request, template_name='kanban/card_detail.html', context={
        'boards': school.school_boards.all(),
        'file_form':file_form,
        'comment_form':comment_form,
        "profile":profile,
        'card':card,
        'metkas': Metka.objects.all(),
        'all_profiles':school.people.filter(is_student=False),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),    
    })

from django.http import JsonResponse
def ChangeCardText(request):
    profile = get_profile(request)
    only_staff(profile)
    if request.GET.get('id'):
        card = Card.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('text'):
            card.description = request.GET.get('text')
            card.save()    
    data = {
        "like_num":0,
    }
    return JsonResponse(data)

def AddUser(request):
    profile = get_profile(request)
    only_staff(profile)
    if request.GET.get('card_id'):
        card = Card.objects.get(id = int(request.GET.get('card_id')))
        if request.GET.get('profile_id'):
            profile = Profile.objects.get(id = int(request.GET.get('profile_id')))
            if request.GET.get('user_in'):
                if request.GET.get('user_in') == 'yes' and profile in card.user_list.all():
                    card.user_list.remove(profile)
                if request.GET.get('user_in') == 'no' and not profile in card.user_list.all():
                    card.user_list.add(profile)
                
    data = {
        "like_num":0,
    }
    return JsonResponse(data)
def AddMetka(request):
    profile = get_profile(request)
    only_staff(profile)
    if request.GET.get('card_id'):
        card = Card.objects.get(id = int(request.GET.get('card_id')))
        if request.GET.get('metka_id'):
            metka = Metka.objects.get(id = int(request.GET.get('metka_id')))
            if request.GET.get('metka_in'):
                if request.GET.get('metka_in') == 'yes' and metka in card.metka_list.all():
                    card.metka_list.remove(metka)
                if request.GET.get('metka_in') == 'no' and not metka in card.metka_list.all():
                    card.metka_list.add(metka)
                
    data = {
        "like_num":0,
    }
    return JsonResponse(data)

def delete_card(request):
    profile = get_profile(request)
    only_staff(profile)
    if not request.user.is_authenticated:
        raise Http404
    card_id = int(request.POST.get('card_delete_id'))
    Card.objects.get(id = card_id).delete()
    return redirect('/todolist')

def delete_column(request):
    profile = get_profile(request)
    only_staff(profile)
    if not request.user.is_authenticated:
        raise Http404
    column_id = int(request.POST.get('column_delete_id'))
    Column.objects.get(id = column_id).delete()
    return redirect('/todolist')

def delete_board(request):
    profile = get_profile(request)
    only_staff(profile)
    if not request.user.is_authenticated:
        raise Http404
    board_id = int(request.POST.get('board_delete_id'))
    Board.objects.get(id = board_id).delete()
    return redirect('/todolist')


def drop(request):
    profile = get_profile(request)
    only_staff(profile)
    payload = json.loads(request.body)
    card_id = int(payload.get('card_id'))
    column_id = int(payload.get('column_id'))
    assert card_id and column_id
    card = Card.objects.get(id=card_id)
    card.column = Column.objects.get(id=column_id)
    card.save()
    return redirect('/todolist')
