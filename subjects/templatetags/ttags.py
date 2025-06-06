from django import template
from ..models import Lecture
register = template.Library()
from django.utils import timezone
import datetime
from datetime import timedelta
from dateutil.relativedelta import *
from itertools import chain
from subjects.models import Day, Cell,Attendance
from squads.models import BillData
from accounts.models import Profession
from schools.models import *

@register.filter
def remove_space(title):
    return title.replace(' ', '_')

@register.filter
def version_date_format(school):
    return school.version_date.strftime('%Y-%m-%d')
@register.filter
def tarif_days_left(school):
    res = (school.version_date.date() - timezone.now().date()).days
    if res <= 0:
        school.version = 'free'
        school.save()
    return res

@register.filter
def is_online(squad):
    return len(squad.subjects.filter(is_online=True)) > 0
@register.filter
def is_individual(squad):
    return len(squad.subjects.filter(is_individual=True)) > 0

@register.filter
def is_no_schedule(squad):
    return len(squad.squad_lectures.all()) == 0

@register.filter
def get_closed_months(nm):
    if len(nm.finance_closed.all()) > 0:
        return nm.finance_closed.first().closed_months
    return 0

@register.filter
def get_start_date(nm):
    return nm.start_date.strftime('%d.%m.%Y')
@register.filter
def get_pay_date(nm):
    return nm.pay_date.strftime('%d %B %Y')

@register.filter
def students_number(squad):
    return len(squad.students.filter(is_student=True))

@register.filter
def filter_actives(managers):
    return len(managers.filter(check_end_work=False))

@register.filter
def payment_notices(profile):
    today = timezone.now().date()
    filter_data = profile.filter_data
    if profile.check_end_work:
        if profile.end_work < timezone.now():
            profile.delete()
    if filter_data.timestamp < today:
        school = profile.schools.first()
        squads = school.groups.filter(shown=True)
        students = school.people.filter(is_student=True, squads__in=squads).exclude(card=None).exclude(squads=None)
        cards = school.crm_cards.filter(card_user__in=students)
        bill_datas = BillData.objects.filter(squad__in=squads, pay_date__lte=today + timedelta(school.bill_day_diff), card__in=cards)
        number = len(cards.filter(bill_data__in=bill_datas).distinct())
        filter_data.payment_notices = number
        filter_data.timestamp = today
        filter_data.save()
    return filter_data.payment_notices

@register.filter
def get_subject_finances(nm):
    res = []
    finances = nm.finance_closed.all().select_related('subject')
    money = nm.money
    for subject in nm.squad.subjects.all():
        period = 'за урок'
        finance = finances.filter(subject=subject)
        date1 = False
        payment = 0
        crnt = 0
        if len(finance) > 0:
            finance = finance[0]
            date1 = finance.first_present.strftime('%d.%m.%Y')
        if subject.cost_period == 'month':
            if finance:
                payment = finance.closed_months
                crnt = finance.moneys[-1]
                period = 'в месяц'
        elif subject.cost_period == 'course':
            period = 'за весь курс'            
        elif subject.cost_period == 'lesson':
            if subject.cost > 0:
                payment = int(money/subject.cost)
            period = 'за урок'
        res.append([
                subject.title,
                str(subject.cost)+'тг '+period,
                payment,
                date1,
                crnt,
                subject.cost_period,
            ])
    return res

@register.filter
def checkdaydif(time, dif):
    return timezone.now() - timedelta(dif) < time

@register.filter
def last_payment(squad, profile):
    res = squad.payment_history.filter(user=profile, canceled=False).first()
    if res:
        return 'Последняя оплата была: '+res.timestamp.strftime('%d.%m.%Y')+' в размере '+str(res.amount)+'тг'
    return 'Еще не было оплаты'

@register.filter
def office_other_managers(office):
    school = office.school
    profession = Profession.objects.get(title = 'Manager')
    filter_data = office.choosed_by.all()
    return school.people.filter(profession=profession).exclude(filter_data__in=filter_data)

@register.filter
def squad_nms_sum(squad):
    res = 0
    for nm in squad.bill_data.all():
        res += nm.money
    return res

@register.filter
def get_filters(subject):
    school = subject.school
    subject_categories = subject.category.all()
    school_categories = SchoolCategory.objects.filter(subject_categories__in=subject_categories)
    f1 = SchoolFilter.objects.filter(mcategories__in=school_categories).prefetch_related('filter_options')
    f2 = SchoolFilter.objects.filter(categories__in=school_categories).prefetch_related('filter_options')
    filters = set(chain(f1, f2))
    ids = [1,7,9,10]
    for i in ids:
        filter1 = SchoolFilter.objects.filter(id=i)
        if len(filter1) > 0:
            filter1 = filter1[0]
            if filter1 in filters:
                filters.remove(filter1)
    return filters

@register.filter
def cell_subject_lectures(cell, subject):
    return Lecture.objects.filter(subject = subject, cell = cell)

@register.filter
def cell_squad_lectures(cell, squad):
    return Lecture.objects.filter(squad = squad, cell = cell)

@register.filter
def cell_profile_lectures(cell, profile):
    return profile.hislectures.filter(cell = cell).select_related('squad').select_related('subject')

def get_pay_date(nm):
    today = timezone.now().date()    
    cnrt_day = today.strftime('%d')
    crnt_mnth = today.strftime('%m')
    crnt_year = today.strftime('%Y') 
    pay_day = nm.pay_day
    nm_date = datetime.datetime.strptime(str(pay_day)+'-'+crnt_mnth+'-'+crnt_year,"%d-%m-%Y").date()
    print('yo', nm_date)
    if nm_date < today:
        pay_date = nm_date + relativedelta(months=1)
    else:
        pay_date = nm_date
    return pay_date

@register.filter
def cell_school_lectures(cell, profile):
    # if profile.filter_data.subject_category==None and profile.skill.crm_age==None and profile.filter_data.office==None:
    #     return []
    lectures = cell.lectures.all()
    # if profile.filter_data.subject_category:
    #     lectures = lectures.filter(category=profile.filter_data.subject_category)
    # if profile.filter_data.office:
    #     lectures = lectures.filter(office=profile.filter_data.office)
    return lectures

@register.filter
def get_date(material, squad):
    if type(material) is str:
        return '_'
    subject = material.subject
    lectures = squad.squad_lectures.filter(subject = subject)
    material_number = list(subject.materials.all()).index(material)+1
    if len(lectures) > 0:
        number_of_weeks = int(material_number/len(lectures))
        lecture_index = material_number % len(lectures)
        if lecture_index == 0:
            number_of_weeks -= 1
            lecture_index = len(lectures)
        if squad.id in subject.squad_ids:
            squad_index = subject.squad_ids.index(squad.id)
        else:
            return '_'
        squad_start_day = subject.start_dates[squad_index]
        start_day = int(squad_start_day.strftime('%w'))
        if start_day == 0:
            start_day = 7
        start_day_object = Day.objects.get(number = start_day)
        if len(lectures.filter(day=start_day_object)) == 0:
            return '_'
        start_day_lecture = lectures.filter(day=start_day_object)[0]
        start_day_index = list(lectures).index(start_day_lecture)
        extra = lectures[(start_day_index + lecture_index-1) % len(lectures)].day.number - start_day
        if extra < 0:
            extra += 7
        x = 7 * number_of_weeks + extra
        date = squad_start_day + timedelta(x)
        
        if date > timezone.now().date():
            check_date = 'future'
        elif date + timedelta(3) >= timezone.now().date():
            check_date = 'now'
        else:
            check_date = 'past'
        return date, check_date
    else:
        return '_'

@register.filter
def get_time(material, profile):
    lectures = profile.hislectures.filter(subject = material.subject)
    if len(lectures) > 0:
        last_week_days = material.number % len(lectures)
        if last_week_days == 0:
            last_week_days = len(lectures)
        time = lectures[last_week_days - 1].cell.time_period
        return time.start + '-' + time.end
    else:
        return '_'

@register.filter
def check_date(material, squad):
    date = get_date(material, squad)
    if date > timezone.now().date():
        return 'future'
    elif date + timedelta(3) >= timezone.now().date():
        return 'now'
    else:
        return 'past'

def material_number_by_date(date, squad, subject, alldays, profile):
    lectures = subject.subject_lectures.filter(squad = squad)        
    num_of_lectures = len(lectures)
    if num_of_lectures > 0:
        delta = (date - squad.start_date).days
        number_of_weeks = int(delta / 7)
        start = int(squad.start_date.strftime('%w'))
        finish = int(date.strftime('%w'))
        search = True
        if start == 0:
            start = 7
        while search:
            day = alldays.get(number=int(start))
            if len(lectures.filter(day=day)) > 0:
                break
            start += 1
            if start > 7:
                start = 1
        if start > finish or finish == 0:
            finish += 7
        extra = 0
        for i in range(start, finish + 1): # Days of week of last not full week
            i = i % 7
            if i == 0:
                i = 7
            day = alldays.get(number=int(i))
            extra += len(lectures.filter(day=day))
        material_number = num_of_lectures * number_of_weeks + extra
        return material_number
    return -1 

@register.filter
def get_current_attendance(subject, squad):
    if not subject or not squad:
        return '_'
    alldays = Day.objects.all()
    material_number = material_number_by_date(timezone.now().date(), squad, subject,alldays, None)
    if material_number >= 0:
        res = []
        i = 0
        counter = 0
        students = squad.students.all()
        subject_materials = subject.materials.all()
        len_squad_students = len(students)
        if material_number > len(subject_materials):
            for i in range(0, material_number - len(subject_materials)):
                subject.materials.create(
                    school=subject.school
                )
            subject.number_of_materials = material_number
            subject.save()
        subject_materials = subject.materials.prefetch_related('sm_atts')
        while material_number - i > 0:
            if counter == 4:
                break
            sm = list(subject_materials)[material_number - i-1]
            if len(sm.sm_atts.filter(squad = squad, student__in=students)) < len_squad_students:
                create_atts(squad, sm, subject)
            attendances = sm.sm_atts.filter(squad = squad, student__in=students)
            get_date_results = '_'
            if len(attendances)>0:
                get_date_results = get_date(attendances[0].subject_materials, squad)
            if get_date_results == '_':
                res = [[attendances, '_','_']] + res
            else:
                res = [[attendances, get_date_results[0], get_date_results[1],sm]] + res
            counter += 1
            i += 1
        if counter < 4:
            i = 1
            while counter < 4 and i < 10 and len(subject_materials) > material_number + i-1:
                sm = list(subject_materials)[material_number + i-1]
                if len(sm.sm_atts.filter(squad = squad, student__in=students)) < len_squad_students:
                    create_atts(squad, sm, subject)
                attendances = sm.sm_atts.filter(squad = squad, student__in=students)
                get_date_results = '_'
                if len(attendances)>0:
                    get_date_results = get_date(attendances[0].subject_materials, squad)
                if get_date_results == '_':
                    res = [[attendances, '_','_']] + res
                    res.append([attendances, '_','_'])
                else:
                    res.append([attendances, get_date_results[0], get_date_results[1]])
                counter += 1
                i += 1
        return res
    else:
        return 'No_schedule'
    return '_'

@register.filter
def get_current_attendance_student(subject, profile):
    if not subject or not profile:
        return '_'
    alldays = Day.objects.all() 
    squad = profile.squads.filter(subjects=subject)[0]
    material_number = material_number_by_date(timezone.now().date(), squad, subject,alldays,profile)
    if material_number >= 0:
        res = []
        i = 0
        counter = 0
        subject_materials = subject.materials.prefetch_related('sm_atts')
        if material_number > len(subject_materials):
            material_number = len(subject_materials)

        while material_number - i > 0:
            if counter == 7:
                break
            sm = list(subject_materials)[material_number - i-1]
            if len(sm.sm_atts.filter(student = profile)) < 1:
                create_atts_student(squad, sm, profile)
            attendances = sm.sm_atts.filter(student = profile)
            get_date_results = get_date(attendances[0].subject_materials, squad)
            if get_date_results == '_':
                res = [[attendances, '_','_']] + res
            else:
                res = [[attendances, get_date_results[0], get_date_results[1]]] + res
            counter += 1
            i += 1
        if counter < 7:
            i = 1
            while counter < 7 and i < 10 and material_number + i-1<len(subject_materials):
                sm = list(subject_materials)[material_number + i-1]
                if len(sm.sm_atts.filter(student = profile)) < 1:
                    create_atts_student(squad, sm, profile)
                attendances = sm.sm_atts.filter(student = profile)
                get_date_results = get_date(attendances[0].subject_materials, squad)
                if get_date_results == '_':
                    res = [[attendances, '_','_']] + res
                    res.append([attendances, '_','_'])
                else:
                    res.append([attendances, get_date_results[0], get_date_results[1]])
                counter += 1
                i += 1
        return res
    return '_'

def create_atts(squad, subject_materials, subject):
    for student in squad.students.all():
        qs = subject_materials.sm_atts.filter(student=student)
        if len(qs) == 0:
            Attendance.objects.get_or_create(
                subject_materials = subject_materials,
                school=subject.school,
                teacher=squad.teacher, 
                student=student,
                subject=subject,
                squad=squad
            )
        else:
            qs[0].squad = squad
            qs[0].save()

def create_atts_student(squad, subject_materials, student):
    Attendance.objects.create(
        subject_materials = subject_materials,
        school=subject_materials.school,
        teacher=squad.teacher, 
        student=student,
        subject=subject_materials.subject,
        squad=squad,
    )

from django.core.paginator import Paginator
@register.filter
def filtercards(column, profile):
    school = profile.schools.first()
    res = []
    if profile.skill:
        if profile.skill.crm_show_free_cards:
            res = column.cards.filter(author_profile=None, school=school).prefetch_related('hashtags')
    if res == []:
        res = column.cards.filter(author_profile=profile, school=school).prefetch_related('hashtags')
    p = Paginator(res, 10)
    page1 = p.page(1)
    return page1.object_list

@register.filter
def filtercardsall(column, profile):
    school = profile.schools.first()
    res = column.cards.filter(school=school).prefetch_related('hashtags').exclude(author_profile__isnull=True).select_related('author_profile')
    p = Paginator(res, 10)
    page1 = p.page(1)
    return page1.object_list

@register.filter
def get_professions(school):
    return chain(Profession.objects.filter(title="Teacher"), Profession.objects.filter(title="Manager"))

@register.filter
def get_jobless_workers(prof, school):
    jobs = prof.job_categories.all()
    return school.people.filter(profession=prof).exclude(job_categories__in=jobs)
@register.filter
def get_jobless_workers_len(prof, school):
    jobs = prof.job_categories.all()
    return len(school.people.filter(profession=prof).exclude(job_categories__in=jobs)) > 0

@register.filter
def get_job_categories(prof, school):
    return school.job_categories.filter(profession=prof)

@register.filter
def get_school_workers(job,school):
    return job.job_workers.filter(schools = school)

@register.filter
def rating_empty_stars(review):
    res = []
    number = 5-review.rating
    if int(number) != number:
        number += 1
    for i in range(0, int(number)):
        res.append(i)
    return res

@register.filter
def get_ratings(school, number):
    return len(school.reviews.filter(rating=number))

@register.filter
def get_subject_courses_len(subject, school):
    return len(school.school_subjects.filter(category=subject))

@register.filter
def get_age_courses_len(age, school):
    return len(school.school_subjects.filter(age=age))

@register.filter
def get_level_courses_len(level, school):
    return len(school.school_subjects.filter(level=level))

@register.filter
def get_column_cards_len(column, school):
    weekago = (timezone.now().date() - timedelta(7)).strftime('%Y-%m-%d')
    return len(school.crm_cards.filter(column=column, timestamp__gt=weekago))

@register.filter
def get_bills(profile, hisprofile):
    school = profile.schools.first()
    squads = hisprofile.squads.filter(school=school).filter(shown=True)
    card = hisprofile.card.filter(school=school)
    if len(card) > 0:
        card = card[0]
        return card.bill_data.filter(squad__in=squads).select_related('squad')
    else:
        return []

@register.filter
def get_bills_len(profile, hisprofile):
    school = profile.schools.first()
    squads = hisprofile.squads.filter(school=school)
    card = hisprofile.card.get(school=school)
    return len(card.bill_data.filter(squad__in=squads).select_related('squad'))

@register.filter
def money_percent(first, second):
    if first+second == 0:
        return 0
    num = first+second
    return int(100*first / num + ((100*first) % num > (num/2)))

@register.filter
def constant_schedule_lectures(squad):
    interval = squad.school.schedule_interval
    res = []
    for lecture in squad.squad_lectures.all():
        hour = int(lecture.cell.time_period.start.split(':')[0]) - 8
        minute = int(lecture.cell.time_period.start.split(':')[1])
        end_hour = int(lecture.cell.time_period.end.split(':')[0]) - 8
        end_minute = int(lecture.cell.time_period.end.split(':')[1])
        height = end_hour - hour + (end_minute - minute)/60
        day = lecture.cell.day.number
        res.append([height, lecture.subject.title, hour,minute, day-1,hour*interval+minute, lecture.id,lecture])
    return res

@register.filter
def constant_profile_lectures(profile):
    teacher = Profession.objects.get(title = 'Teacher')
    if teacher in profile.profession.all():
        squads = profile.hissquads.filter(shown=True)
    else:
        squads = profile.squads.filter(shown=True)
    lectures = Lecture.objects.filter(squad__in=squads).select_related('cell')
    #lectures = profile.hislectures.select_related('cell')
    interval = 60
    res = []
    for lecture in lectures:
        hour = int(lecture.cell.time_period.start.split(':')[0]) - 8
        minute = int(lecture.cell.time_period.start.split(':')[1])
        end_hour = int(lecture.cell.time_period.end.split(':')[0]) - 8
        end_minute = int(lecture.cell.time_period.end.split(':')[1])
        height = end_hour - hour + (end_minute - minute)/60
        day = lecture.cell.day.number
        res.append([height, lecture.subject.title, hour,minute, day-1,hour*interval+minute, lecture.id,lecture])
    return res

@register.filter
def constant_school_lectures(profile, school):
    squads = school.groups.filter(shown=True)
    lectures = Lecture.objects.filter(squad__in=squads)
    # if profile.filter_data.subject_category:
    #     lectures = lectures.filter(category=profile.filter_data.subject_category)
    # if profile.filter_data.office:
    #     lectures = lectures.filter(office=profile.filter_data.office)
    if profile.filter_data.teacher:
        teacher = profile.filter_data.teacher
        squads = teacher.hissquads.all()
        lectures = lectures.filter(squad__in=squads)
    if profile.filter_data.subject:
        lectures = lectures.filter(subject=profile.filter_data.subject)
    if profile.filter_data.subject_type != 'all':
        if profile.filter_data.subject_type == 'individual':
            subjects = school.school_subjects.filter(is_individual=True)
        elif profile.filter_data.subject_type == 'regular':
            subjects = school.school_subjects.filter(is_individual=False, is_online=False)
        elif profile.filter_data.subject_type == 'online':
            subjects = school.school_subjects.filter(is_online=True)
        lectures = lectures.filter(subject__in=subjects)

    res = []
    interval = school.schedule_interval
    for lecture in lectures.order_by('cell'):
        start = lecture.cell.time_period.start.split(':')
        hour = int(start[0]) - 8
        minute = int(start[1])
        end = lecture.cell.time_period.end.split(':')
        end_hour = int(end[0]) - 8
        end_minute = int(end[1])
        height = end_hour - hour + (end_minute - minute)/60
        day = lecture.cell.day.number
        subject = lecture.subject
        if subject.cost_period == 'month':
            subject_period = 'в месяц'
        elif  subject.cost_period == 'lesson':
            subject_period = 'за урок'
        elif  subject.cost_period == 'course':
            subject_period = 'за курс'
        else:
            subject_period = ''
        squad = lecture.squad
        if squad.color_back == '':
            color_back = '#313a57'
        else:
            color_back = squad.color_back
        teacher = ''
        if squad.teacher:
            teacher = squad.teacher.first_name
        res.append([
            height,                 #0
            subject.title,          #1
            hour,                   #2
            minute,                 #3
            day-1,                  #4
            hour*interval+minute,   #5
            lecture.id,             #6
            lecture.squad.id,       #7
            str(subject.cost) + 'тг '+subject_period, #8
            color_back,             #9
            squad.title,            #10
            teacher,                #11
            ])
    return res
