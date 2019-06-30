from django import template
from ..models import Lecture
register = template.Library()
from django.utils import timezone
from datetime import timedelta
from itertools import chain
from subjects.models import Day, Cell,Attendance
from accounts.models import Profession

@register.filter
def cell_subject_lectures(cell, subject):
    return Lecture.objects.filter(subject = subject, cell = cell)

@register.filter
def cell_squad_lectures(cell, squad):
    return Lecture.objects.filter(squad = squad, cell = cell)

@register.filter
def cell_profile_lectures(cell, profile):
    return profile.hislectures.filter(cell = cell).select_related('squad').select_related('subject')

@register.filter
def rating_filter(profile):
    school = profile.schools.first()
    squad = profile.rating_squad_choice.first()
    crm_subject_students = None
    crm_age_students = None
    if profile.skill.crm_subject:
        crm_subject_students = profile.skill.crm_subject.students.all()
    if profile.skill.crm_age:
        crm_age_students = profile.skill.crm_age.students.all()
    if squad != None:
        students_query = squad.students.all()
    else:
        students_query = school.people.filter(is_student=True)
    res = []
    for student in students_query:
        need = True
        if crm_subject_students != None:
            if not student in crm_subject_students:
                need = False
        if crm_age_students != None:
            if not student in crm_age_students:
                need = False
        if need:
            res.append(student)

    return res

@register.filter
def cell_school_lectures(cell, profile):
    # if profile.skill.crm_subject==None and profile.skill.crm_age==None and profile.skill.crm_office==None:
    #     return []
    print(profile.skill.crm_subject, profile.skill.crm_age, profile.skill.crm_office)
    lectures = cell.lectures.all()
    if profile.skill.crm_subject:
        lectures = lectures.filter(category=profile.skill.crm_subject)
    if profile.skill.crm_age:
        lectures = lectures.filter(age=profile.skill.crm_age)
    if profile.skill.crm_office:
        lectures = lectures.filter(office=profile.skill.crm_office)
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
        elif date + timedelta(17) >= timezone.now().date():
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
    if num_of_lectures > 0 and  timezone.now().date() > squad.start_date:
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
    elif date + timedelta(17) >= timezone.now().date():
        return 'now'
    else:
        return 'past'

@register.filter
def get_current_attendance(subject, squad):
    if not subject or not squad:
        return '_'
    lectures = squad.squad_lectures.filter(subject = subject)
    num_of_lectures = len(lectures)
    if num_of_lectures > 0 and  timezone.now().date() > squad.start_date:
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
        material_number = num_of_lectures * number_of_weeks + extra
        res = []
        i = 0
        counter = 0
        subject_materials = subject.materials.prefetch_related('sm_atts')
        len_squad_students = len(squad.students.all())
        if material_number > len(subject_materials):
            material_number = len(subject_materials)
        while material_number - i > 0:
            if counter == 4:
                break
            sm = list(subject_materials)[material_number - i-1]
            if len(sm.sm_atts.filter(squad = squad)) < len_squad_students:
                create_atts(squad, sm, subject)
            attendances = sm.sm_atts.filter(squad = squad)
            get_date_results = get_date(attendances[0].subject_materials, squad)
            if get_date_results == '_':
                res = [[attendances, '_','_']] + res
            else:
                res = [[attendances, get_date_results[0], get_date_results[1]]] + res
            counter += 1
            i += 1
        if counter < 4:
            i = 1
            while counter < 4 and i < 10 and len(subject_materials) > material_number + i-1:
                sm = list(subject_materials)[material_number + i-1]
                if len(sm.sm_atts.filter(squad = squad)) < len_squad_students:
                    create_atts(squad, sm, subject)
                attendances = sm.sm_atts.filter(squad = squad)
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

@register.filter
def get_current_attendance_student(subject, profile):
    if not subject or not profile:
        return '_'
    squad = profile.squads.filter(subjects=subject)
    if len(squad)>0:
        squad = squad[0]
    lectures = profile.hislectures.filter(subject = subject)
    num_of_lectures = len(lectures)
    if num_of_lectures > 0 and  timezone.now().date() > squad.start_date:
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
        material_number = num_of_lectures * number_of_weeks + extra
        res = []
        i = 0
        counter = 0
        subject_materials = subject.materials.prefetch_related('sm_atts')
        if material_number > len(subject_materials):
            material_number = len(subject_materials)
        while material_number - i > 0:
            if counter == 4:
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
        if counter < 4:
            i = 1
            while counter < 4 and i < 10:
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
            Attendance.objects.create(
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

@register.filter
def filtercards(column, profile):
    if profile.skill:
        if profile.skill.crm_show_free_cards:
            return column.cards.filter(author_profile=None).prefetch_related('hashtags')
    return column.cards.filter(author_profile=profile).prefetch_related('hashtags')

@register.filter
def get_professions(school):
    return Profession.objects.all()

@register.filter
def get_school_workers(job,school):
    return job.job_workers.filter(schools = school)
