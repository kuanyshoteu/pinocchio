from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import dateutil.parser
from datetime import timedelta
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from .forms import *
from .models import *
from squads.models import *
from todolist.models import *
from subjects.models import *
from django.contrib.auth.forms import PasswordChangeForm
from schools.models import School
from constants import *
from subjects.templatetags.ttags import get_date, check_date, create_atts, create_atts_student

def test_account(request):
    profile = Profile.objects.get(id = 621) #621
    hisprofile = profile
    skill = hisprofile.skill
    miss_lesson_form = False
    mypage = ''
    if profile == hisprofile:
        mypage = 'mypage'
        # Нужна отдельная функция при вызове
        miss_lesson = MissLesson.objects.filter(profile = profile)
        if len(miss_lesson) > 0:
            miss_lesson = miss_lesson[0]
            miss_lesson_form = MissLessonForm(request.POST or None, request.FILES or None, instance=miss_lesson)
        else:
            miss_lesson_form = MissLessonForm(request.POST or None, request.FILES or None)
        if miss_lesson_form.is_valid():
            miss_lesson = miss_lesson_form.save()
    hissubjects = []
    if is_profi(hisprofile, 'Manager'):
        if profile.skill.crm_office2:
            hissquads = profile.skill.crm_office2.groups.filter(shown=True)
        else:
            hissquads =  profile.schools.first().groups.filter(shown=True)
    elif is_profi(hisprofile, 'Teacher'):
        hissquads = hisprofile.hissquads.filter(shown=True)
    else:
        hissquads = hisprofile.squads.filter(shown=True)
        hissubjects = set(Subject.objects.filter(squads__in=hissquads))
    hiscacheatt = CacheAttendance.objects.get_or_create(profile = hisprofile)[0]

    school_money = 0
    is_director = is_profi(profile, 'Director')
    if is_director:
        school_money = profile.schools.first().money
    context = {
        "profile":profile,
        "hisprofile": hisprofile,
        'att_subject':hiscacheatt.subject,
        'att_squad':hiscacheatt.squad,
        'today':int(timezone.now().date().strftime('%w')),
        'hissquads':hissquads,
        'hissubjects':hissubjects,
        'miss_lesson_form':miss_lesson_form,
        'is_this_trener':is_profi(hisprofile, 'Teacher'),
        "is_this_manager":is_profi(hisprofile, 'Manager'),
        "is_this_director":is_profi(hisprofile, 'Director'),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_director,
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school_money,
        'constant_times':get_times(60),
        "interval":60,
        'height':28*15+25, 
        "page":mypage,       
    }
    return render(request, "profile.html", context)

def account_view(request, user = None):
    profile = get_profile(request)
    user = user.replace('_', ' ')
    user = User.objects.get(username = user)
    hisprofile = Profile.objects.get(user = user)
    skill = hisprofile.skill
    if profile.skill.confirmed == False:
        return redirect(profile.check_confirmation())
    miss_lesson_form = False
    mypage = ''
    if profile == hisprofile:
        mypage = 'mypage'
        # Нужна отдельная функция при вызове
        miss_lesson = MissLesson.objects.filter(profile = profile)
        if len(miss_lesson) > 0:
            miss_lesson = miss_lesson[0]
            miss_lesson_form = MissLessonForm(request.POST or None, request.FILES or None, instance=miss_lesson)
        else:
            miss_lesson_form = MissLessonForm(request.POST or None, request.FILES or None)
        if miss_lesson_form.is_valid():
            miss_lesson = miss_lesson_form.save()
            return check_confirmation(hisprofile, skill)
    hissubjects = []
    hissquads = []
    hiscacheatt = CacheAttendance.objects.get_or_create(profile = hisprofile)[0]
    if is_profi(hisprofile, 'Director'):
        hissquads = profile.schools.first().groups.filter(shown=True)
    elif is_profi(hisprofile, 'Manager'):
        if profile.skill.crm_office2:
            hissquads = profile.skill.crm_office2.groups.filter(shown=True)
    elif is_profi(hisprofile, 'Teacher'):
        hissquads = hisprofile.hissquads.filter(shown=True)
    else:
        hissquads = hisprofile.squads.filter(shown=True)
    if len(hissquads) > 0:
        if not hiscacheatt.squad in hissquads:
            hiscacheatt.squad = hissquads.first()
        if not hiscacheatt.subject in hiscacheatt.squad.subjects.all():
            hiscacheatt.subject = hiscacheatt.squad.subjects.first()
    else:
        hiscacheatt.squad = None
        hiscacheatt.subject = None
    hiscacheatt.save()
    att_squad = hiscacheatt.squad
    if is_profi(hisprofile, 'Manager'):
        if profile.skill.crm_office2:
            if att_squad in hissquads:
                hissubjects = att_squad.subjects.all()
        else:
            if att_squad in hissquads:
                hissubjects = att_squad.subjects.all()
    else:
        hissubjects = set(Subject.objects.filter(squads__in=hissquads))

    school_money = 0
    if len(profile.schools.all()) > 0:
        school = profile.schools.first()
    else:
        school = None
    is_director = is_profi(profile, 'Director')
    if is_director:
        school_money = profile.schools.first().money
    context = {
        "profile":profile,
        "hisprofile": hisprofile,
        'att_subject':hiscacheatt.subject,
        'att_squad':att_squad,
        'today':int(timezone.now().date().strftime('%w')),
        'hissquads':hissquads,
        'hissubjects':hissubjects,
        'miss_lesson_form':miss_lesson_form,
        'is_this_trener':is_profi(hisprofile, 'Teacher'),
        "is_this_manager":is_profi(hisprofile, 'Manager'),
        "is_this_director":is_profi(hisprofile, 'Director'),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_director,
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school_money,
        "school_crnt":school,
        'constant_times':get_times(60),
        "interval":60,
        'height':28*15+25, 
        "page":mypage,       
    }
    return render(request, "profile.html", context)

def check_confirmation(request):
    profile = get_profile(request)  
    skill = profile.skill
    if skill.confirmed == False:
        if timezone.now() - skill.confirmation_time:
            skill.confirmation_code = random_secrete_confirm()
            skill.confirmation_time = timezone.now()
            skill.save()
            url = request.build_absolute_uri().replace(request.get_full_path(), '') + '/confirm/?confirm='+profile.skill.confirmation_code
            text = "Здравствуйте "+profile.first_name+ "!<br><br> Вы зарегестрировались на сайте Bilimtap.kz, для подтверждения вашего Email пожалуйста пройдите по ссылке: "
            html_content = text + "<br><a href='"+url+"'>подтвердить</a>"
            try:
                send_email("Подтверждение", html_content, [profile.mail])
            except Exception as e:
                pass
        context = {
            "profile": profile,
        }
        return render(request, "confirm.html", context)
    else:
        return redirect(profile.get_absolute_url())

def hisboards(hisprofile):
    hisboards = []
    if is_profi(hisprofile, 'Student') == False:
        for school in hisprofile.schools.all():
            for board in school.school_boards.all():
                hiscolumns = []
                for column in board.columns.all():
                    hiscards = []
                    for card in column.cards.all():
                        if hisprofile in card.user_list.all():
                            hiscards.append(card)
                    if len(hiscards) > 0:
                        hiscolumns.append([column, hiscards])
                if len(hiscolumns) > 0:
                    hisboards.append([board, hiscolumns])
    return(hisboards)

def save_profile(request):
    profile = get_profile(request)
    if request.GET.get('name'):
        profile.first_name = request.GET.get('name')
        profile.mail = request.GET.get('mail')
        profile.phone = request.GET.get('phone')
        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')
        profile.save()
    data = {
    }
    return JsonResponse(data)

def change_profile(request):
    profile = get_profile(request)
    form = ProfileForm(request.POST or None, request.FILES or None,instance=profile)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.save()
    school = profile.schools.all()
    school_money = 0
    if len(school) > 0:
        school = school[0]
        school_money = school.money
    context = {
        "profile":profile, 
        'form':form,
        "school_crnt":school,        
        "school_money":school_money,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "profile/change_profile.html", context)

def confirm_email(request):
    if request.GET.get('confirm'):
        profile = Profile.objects.get(user = request.user)
        skill = profile.skill
        if skill.confirmation_code == request.GET.get('confirm'):
            skill.confirmed = True
            skill.save()
    return redirect(profile.get_absolute_url())

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def subject_attendance(request):
    if request.GET.get('subject_id'):
        profile = Profile.objects.get(user = request.user)
        cache_att = CacheAttendance.objects.get_or_create(profile=profile)[0]
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')))
        school = subject.school
        is_in_school(profile, school)
        cache_att.subject = subject
        cache_att.save()
    data = {
    }
    return JsonResponse(data)
def squad_attendance(request):
    if request.GET.get('squad_id'):
        profile = Profile.objects.get(user = request.user)
        cache_att = CacheAttendance.objects.get(profile=profile)
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')))
        school = squad.school
        is_in_school(profile, school)
        cache_att.squad = squad
        if not cache_att.subject in squad.subjects.all():
            cache_att.subject = squad.subjects.first()
        cache_att.save()
    data = {
    }
    return JsonResponse(data)

def more_attendance(request):
    profile = Profile.objects.get(user = request.user)
    if request.GET.get('subject_id') and request.GET.get('squad_id') and request.GET.get('direction') and request.GET.get('sm_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')))
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')))
        school = subject.school
        is_in_school(profile, school)
        current_sm = int(request.GET.get('sm_id'))
        columns = []
        last_set = False
        first_set = False
        stopleft = False
        stopright = False
        if request.GET.get('direction') == 'left':
            queryset = subject.materials.filter(id__lt = current_sm).order_by('-id')
            if len(queryset) <= 4:
                first_set = True
                if len(queryset) == 0:
                    stopleft = True
            for sm in queryset:
                if len(columns) == 4:
                    break
                if len(sm.sm_atts.filter(squad = squad)) < len(squad.students.all()):
                    create_atts(squad, sm, subject)
                get_date_results = get_date(sm, squad)
                if get_date_results == '_':
                    section = ['_', sm.id, '_']
                else:
                    section = [get_date_results[0].strftime('%d %B %Y'), sm.id, get_date_results[1]]
                for att in sm.sm_atts.filter(squad = squad):
                    section.append([att.id, att.present, att.grade])
                columns.append(section)
        else:
            queryset = subject.materials.filter(id__gt = current_sm)
            if len(queryset) <= 4:
                last_set = True
                if len(queryset) == 0:
                    stopright = True                
            for sm in queryset:
                if len(columns) == 4:
                    break
                section = [get_date(sm, squad)[0].strftime('%d %B %Y'), sm.id]
                columns.append(section)
        data = {
            'first_set':first_set,
            'last_set':last_set,
            'columns':columns,
            'stopleft':stopleft,
            'stopright':stopright,
        }
        return JsonResponse(data)

def more_attendance_student(request):
    profile = get_profile(request)
    if request.GET.get('subject_id') and request.GET.get('direction') and request.GET.get('sm_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')))
        squad = subject.squads.filter(students=profile)[0]
        school = subject.school
        is_in_school(profile, school)
        current_sm = int(request.GET.get('sm_id'))
        columns = []
        last_set = False
        first_set = False
        if request.GET.get('direction') == 'left':
            queryset = subject.materials.filter(id__lt = current_sm).order_by('-id')
            if len(queryset) <= 4:
                first_set = True
            for sm in queryset:
                if len(columns) == 4:
                    break
                if len(sm.sm_atts.filter(student = profile)) < 1:
                    create_atts_student(squad, sm, profile)
                section = [get_date(sm, squad)[0], sm.id, 'past']
                att = sm.sm_atts.get(student = profile)
                section.append([att.id, att.present, att.grade])
                columns.append(section)
        else:
            queryset = subject.materials.filter(id__gt = current_sm)
            if len(queryset) <= 4:
                last_set = True
            for sm in queryset:
                if len(columns) == 4:
                    break
                section = [get_date(sm, squad)[0], sm.id]
                columns.append(section)
        data = {
            'first_set':first_set,
            'last_set':last_set,
            'columns':columns,
        }
        return JsonResponse(data)

def miss_lecture(request):
    profile = Profile.objects.get(user = request.user)
    if request.GET.get('date'):
        miss_lesson = MissLesson.objects.filter(profile = profile)
        if len(miss_lesson) > 0:
            miss_lesson = miss_lesson[0]
        else:
            miss_lesson = MissLesson.objects.create(profile=profile)
        date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
        if date in miss_lesson.dates:
            action = 'remove'
            miss_lesson.dates.remove(date)
        else:
            action = 'add'
            miss_lesson.dates.append(date)
        miss_lesson.save()

    data = {
        'action':action
    }
    return JsonResponse(data)

def att_present(request):
    profile = Profile.objects.get(user = request.user)
    only_staff(profile)
    ok = False
    teacher_attendance_id = -1
    if request.GET.get('id') and request.GET.get('status'):
        attendance = Attendance.objects.get(id = int(request.GET.get('id')))
        school = attendance.school
        subject = attendance.subject
        squad = attendance.squad
        is_in_school(profile, school)
        profile = squad.teacher
        ok = True
        material = attendance.subject_materials
        need_change_school_money = False
        card = attendance.student.card.get_or_create(school=school)[0]
        if request.GET.get('status') == 'present':
            attendance.present = 'present'
            attendance.save()
            ##### Teacher made lesson
            teacher_attendance = material.sm_atts.filter(student=profile)
            if len(teacher_attendance):
                teacher_attendance = teacher_attendance[0]
                teacher_attendance.present = 'present'
                teacher_attendance.save()
                teacher_attendance_id = teacher_attendance.id
            ##### Move CRMCard in columns
            if card.column:
                if card.column.id == 2:
                    card.column = CRMColumn.objects.get(id=3)
                    card.save()
            ##### Teacher salary increase
            salary = 0
            if not profile in material.done_by.all():
                material.done_by.add(profile)
                profile.money += profile.salary
                salary = -1*profile.salary
                need_change_school_money = True
            cost = subject.cost
        elif request.GET.get('status') == 'cancel':
            att_present_was = attendance.present
            attendance.present = ''
            attendance.save()
            if len(material.sm_atts.filter(squad=squad,present='present')) == 0:
                if profile in material.done_by.all():
                    material.done_by.remove(profile)
                    profile.money -= profile.salary
                if att_present_was == 'present':
                    need_change_school_money = True
                    salary = profile.salary
                    cost = -1*subject.cost
        if request.GET.get('status') == 'cancel' or request.GET.get('status') == 'present':
            #### Update first presence in squad and subject
            if subject.cost_period == 'month' and subject.cost > 0:
                date1 = get_date(attendance.subject_materials, squad)[0]
                nm = card.need_money.filter(squad=squad)
                need_fc = False
                if len(nm) > 0:
                    nm = nm[0]
                    fc = nm.finance_closed.filter(subject=subject)
                    if len(fc) == 0:
                        need_fc = True
                    else:
                        fc = fc[0]
                else:
                    nm = card.need_money.create(squad=squad,start_date=date1)
                    need_fc = True
                    nm.save()
                if need_fc:
                    fc = nm.finance_closed.create(subject=subject,
                        moneys=[0],
                        bills=[subject.cost],
                        start=date1,
                        first_present=date1,
                        pay_date=date1,)
                if len(subject.subject_attendances.filter(student=attendance.student,squad=squad,present='present')) == 1:
                    if request.GET.get('status') == 'present':
                        fc.first_present=date1
                        fc.save()
            if need_change_school_money:
                change_school_money(school, salary, 'teacher_salary', profile.first_name)
                school.save()
                cards = school.crm_cards.all()
                if subject.cost_period == 'lesson':
                    for at in material.sm_atts.exclude(present='warned'):
                        student = at.student
                        card = cards.filter(card_user=student)
                        if len(card) > 0:
                            pay_for_lesson(card[0], cost, squad)
        else:            
            attendance.present = request.GET.get('status')
            attendance.save()        
        profile.save()
    data = {
        'ok':ok,
        'teacher_id':teacher_attendance_id,
    }
    return JsonResponse(data)

def pay_for_lesson(card, cost, squad):
    nm = squad.need_money.filter(card=card)
    if len(nm) > 0:
        nm = nm[0]
        nm.money -= int(cost)
        if nm.money < squad.lesson_bill:
            card.color = 'red'
            if card.was_called:
                skill = card.author_profile.skill
                skill.need_actions += 1
                skill.save()
                card.was_called = False
        elif nm.money < 2 * squad.lesson_bill:
            card.color = 'orange'
            if card.was_called:
                skill = student_card.author_profile.skill
                skill.need_actions += 1
                skill.save()
                card.was_called = False
        elif nm.money >= 2 * squad.lesson_bill:
            card.color = ''
        card.save()
        nm.save()
    else:
        Bug.objects.create(text='No NeedMoney object of card ' + card.id)

def ChangeAttendance(request):
    profile = Profile.objects.get(user = request.user)
    if request.GET.get('id'):
        attendance = Attendance.objects.get(id = int(request.GET.get('id')))
        school = attendance.school
        is_in_school(profile, school)        
        if request.GET.get('grade'):
            attendance.grade = int(request.GET.get('grade'))
        attendance.save()
    data = {
    }
    return JsonResponse(data)

def tell_about_corruption(request):
    profile = Profile.objects.get(user = request.user)
    ok = False
    if request.GET.get('text'):
        Corruption.objects.create(text=request.GET.get('text'),author_profile=profile, school=profile.school)
        ok = True
    data = {
        'ok':ok
    }
    return JsonResponse(data)

def another_hint(request):
    profile = Profile.objects.get(user = request.user)
    hint_type = int(request.GET.get('hint_type'))
    if request.GET.get('dir') == 'next':
        profile.skill.hint_numbers[hint_type] += 1
    elif request.GET.get('dir') == 'prev':
        profile.skill.hint_numbers[hint_type] -= 1
    else:
        profile.skill.hint_numbers[hint_type] = 100
    profile.skill.save()
    data = {
    }
    return JsonResponse(data)

def logout_view(request):
    logout(request)
    return redirect("/")

def add_money(profile, school, squad, card, amount, manager):
    if amount > squad.bill*10:
        return 'too much'
    nm = card.need_money.get(squad=squad)
    nm.money += amount
    nm.save()
    crnt = amount
    today = timezone.now().date()
    ok = True
    subjects = squad.subjects.filter(cost_period='month', cost__gt=0)
    while crnt > 0:
        for subject in subjects:
            if crnt <= 0:
                break
            fc = nm.finance_closed.filter(subject=subject)
            if len(fc) > 0:
                fc = fc[0]
            elif len(fc) == 0:
                fc = nm.finance_closed.create(
                    subject=subject,
                    start=today,
                    first_present=today,
                    moneys=[0],
                    bills=[subject.cost],
                    pay_date=today,)
            added_money = min(subject.cost - fc.moneys[-1], crnt)
            fc.moneys[-1] += added_money
            crnt -= added_money
            finance_update_month(fc, subject.cost)
            fc.save()
    if ok:
        if card.color == 'red' or card.color == 'orange':
            if not card.was_called:
                skill = card.author_profile.skill
                skill.need_actions -= 1
                skill.save()
        card.color = 'white'
        card.save()
    canceled = False
    if amount < 0:
        canceled = True
    profile.payment_history.create(
        action_author = manager,
        amount = amount,
        school = school,
        squad = squad,
        canceled = canceled,
    )
    change_school_money(school, amount, 'student_payment', profile.first_name)
    school.save()

def finance_update_month(fc, subject_cost):
    if fc.moneys[-1] >= fc.bills[-1]:
        fc.moneys.append(0)
        fc.bills.append(subject_cost)
        fc.closed_months += 1
        ok = True
        fc.save()

def make_payment(request):
    manager = Profile.objects.get(user = request.user)
    only_managers(manager)
    amount = int(request.GET.get('amount'))
    if amount > 0 and request.GET.get('id') and request.GET.get('group_id'):
        profile = Profile.objects.get(id = int(request.GET.get('id')))
        school = manager.schools.first()
        squad = school.groups.get(id=int(request.GET.get('group_id')))
        card = profile.card.get(school=school)
        add_money(profile, school, squad, card, amount, manager)
    data = {
    }
    return JsonResponse(data)

def make_payment_card(request):
    manager = Profile.objects.get(user = request.user)
    only_managers(manager)
    amount = 0
    if request.GET.get('amount'):
        amount = int(request.GET.get('amount'))
    bills = []
    if amount > 0 and request.GET.get('id') and request.GET.get('group_id'):
        card = CRMCard.objects.get(id = int(request.GET.get('id')))
        profile = card.card_user
        school = manager.schools.first()
        squad = school.groups.get(id=int(request.GET.get('group_id')))
        add_money(profile, school, squad, card, amount, manager)
        nms = card.need_money.select_related('squad')
        for squad in profile.squads.all():
            crnt = nms.filter(squad=squad)
            if len(crnt) > 0:
                crnt = crnt[0]
                bills.append([squad.title, crnt.money, squad.lesson_bill, squad.bill,squad.id])
    data = {
        'bills':bills,
    }
    return JsonResponse(data)
