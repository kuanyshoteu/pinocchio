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
def payment_notices(profile):
    today = timezone.now().date()
    filter_data = profile.filter_data
    print('8888888888888888')
    print(filter_data.timestamp, today)
    if filter_data.timestamp < today:
        print('7777777777')
        school = profile.schools.first()
        squads = school.groups.filter(shown=True)
        print(squads)
        number = len(BillData.objects.filter(squad__in=squads, pay_date__lte=today + timedelta(school.bill_day_diff)))
        filter_data.payment_notices = number
        print(number)
        print('55555555555')
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
    if profile.filter_data.subject_category:
        lectures = lectures.filter(category=profile.filter_data.subject_category)
    if profile.skill.crm_age:
        lectures = lectures.filter(age=profile.skill.crm_age)
    if profile.filter_data.office:
        lectures = lectures.filter(office=profile.filter_data.office)
    return lectures

@register.filter
def get_date(material, squad):
    if type(material) is str:
        print('0')
        return '_'
    subject = material.subject
    lectures = squad.squad_lectures.filter(subject = subject)
    material_number = list(subject.materials.all()).index(material)+1
    if len(lectures) > 0:
        print('1')
        number_of_weeks = int(material_number/len(lectures))
        lecture_index = material_number % len(lectures)
        if lecture_index == 0:
            print('2')
            number_of_weeks -= 1
            lecture_index = len(lectures)
        if squad.id in subject.squad_ids:
            print('3')
            squad_index = subject.squad_ids.index(squad.id)
        else:
            return '_'
        squad_start_day = subject.start_dates[squad_index]
        start_day = int(squad_start_day.strftime('%w'))
        if start_day == 0:
            start_day = 7
        start_day_object = Day.objects.get(number = start_day)
        print('d',lectures.filter(day=start_day_object))
        if len(lectures.filter(day=start_day_object)) == 0:
            print('4')
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
def get_material(subject, profile):
    lectures = profile.hislectures.filter(subject = subject)
    num_of_lectures = len(lectures)
    if profile.is_student:
        squad = profile.squads.filter(subjects=subject)
    else:
        squad = profile.hissquads.filter(subjects=subject)
    if len(squad) > 0:
        squad = squad[0]
    if num_of_lectures > 0 and timezone.now().date() >= squad.start_date:
        delta = (timezone.now().date() - squad.start_date).days
        number_of_weeks = int(delta / 7)
        finish = delta % 7
        start = int(squad.start_date.strftime('%w'))
        if start == 0:
            start = 7
        if start > finish or finish == 0:
            finish += 7
        extra = 0
        for i in range(start, finish + 1): # Days of week of last not full week
            i = i % 7
            if i == 0:
                i = 7
            day=Day.objects.get(number=int(i))
            extra += len(lectures.filter(day=day))
        material_number = num_of_lectures * number_of_weeks + extra + 1
        if len(subject.materials.filter(number = material_number)) > 0:
            return subject.materials.filter(number = material_number)[0].lessons.all()
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
    if profile == None:
        lectures = squad.squad_lectures.filter(subject = subject)
    else:
        lectures = subject.subject_lectures.filter(squad = squad)        
    num_of_lectures = len(lectures)
    if num_of_lectures > 0:
        delta = (date - squad.start_date).days
        number_of_weeks = int(delta / 7)
        start = int(squad.start_date.strftime('%w'))
        finish = int(timezone.now().date().strftime('%w'))
        search = True
        if start == 0:
            start = 7
        while search:
            day=alldays.get(number=int(start))
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
            day=alldays.get(number=int(i))
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
        print(material_number, len(subject_materials))
        if material_number > len(subject_materials):
            print('gere')
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
            print(get_date_results)
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
        print('******',lecture.id, lecture.cell.time_period.start)
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
    if profile.filter_data.subject_category:
        lectures = lectures.filter(category=profile.filter_data.subject_category)
    if profile.filter_data.office:
        lectures = lectures.filter(office=profile.filter_data.office)
    if profile.filter_data.teacher:
        teacher = profile.filter_data.teacher
        squads = teacher.hissquads.all()
        lectures = lectures.filter(squad__in=squads)
    if profile.filter_data.subject:
        lectures = lectures.filter(subject=profile.filter_data.subject)
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
