from django import template
from ..models import Lecture
register = template.Library()
from django.utils import timezone
from datetime import timedelta
from itertools import chain
from subjects.models import Day, Cell,Attendance

@register.filter
def findorder(material, profile):
    # llist = profile.curators_squads.first().cells.filter(subject_materials=material)
    # if len(llist)>0:
    #     return [llist[0].date, ' ' + llist[0].time_period.start +'-'+ llist[0].time_period.end]
    return 'de'

@register.filter
def check_material_date(material, profile):
    # llist = profile.squads.first().cells.filter(subject_materials=material)
    # if len(llist)>0:
    #     date = llist[0].date
    #     if date < timezone.now().date():
    #         return True
    return False

@register.filter
def cell_subject_lectures(cell, subject):
    return Lecture.objects.filter(subject = subject, cell = cell)

@register.filter
def cell_squad_lectures(cell, squad):
    return Lecture.objects.filter(squad = squad, cell = cell)

@register.filter
def cell_profile_lectures(cell, profile):
    return profile.hislectures.filter(cell = cell)

@register.filter
def cell_school_lectures(cell, profile):
    lectures = cell.lectures.all()
    if profile.crm_subject:
        lectures = lectures.filter(category=profile.crm_subject)
    if profile.crm_age:
        lectures = lectures.filter(age=profile.crm_age)
    if profile.crm_office:
        lectures = lectures.filter(office=profile.crm_office)
    return lectures

@register.filter
def get_date(material, squad):
    if type(material) is str:
        return '_'
    subject = material.subject
    lectures = squad.squad_lectures.filter(subject = subject)
    if len(lectures) > 0:
        number_of_weeks = int(material.number/len(lectures))
        lecture_index = material.number % len(lectures)
        if lecture_index == 0:
            number_of_weeks -= 1
            lecture_index = len(lectures)
        if squad.id in subject.squad_ids:
            squad_index = subject.squad_ids.index(squad.id)
        else:
            return '_'
        start_day = int(subject.start_dates[squad_index].strftime('%w'))
        if start_day == 0:
            start_day = 7
        start_day_object = Day.objects.get(number = start_day)
        start_day_lecture = lectures.filter(day=start_day_object)[0]
        start_day_index = list(lectures).index(start_day_lecture)
        #print(start_day_index , lecture_index)
        extra = lectures[(start_day_index + lecture_index-1) % len(lectures)].day.number - start_day
        if extra < 0:
            extra += 7
        x = 7 * number_of_weeks + extra
        date = subject.start_dates[squad_index] + timedelta(x)
        #print(material.number, date, 'weeks', number_of_weeks, 'extra', extra)
        return date
    else:
        return '_'

@register.filter
def get_date_student(material, squad):
    if type(material) is str:
        return '_'
    subject = material.subject
    lectures = squad.squad_lectures.filter(subject = subject)
    if len(lectures) > 0:
        number_of_weeks = int(material.number/len(lectures))
        lecture_index = material.number % len(lectures)
        if lecture_index == 0:
            number_of_weeks -= 1
            lecture_index = len(lectures)
        if squad.id in subject.squad_ids:
            squad_index = subject.squad_ids.index(squad.id)
        else:
            return '_'
        start_day = int(subject.start_dates[squad_index].strftime('%w'))
        if start_day == 0:
            start_day = 7
        start_day_object = Day.objects.get(number = start_day)
        start_day_lecture = lectures.filter(day=start_day_object)[0]
        start_day_index = list(lectures).index(start_day_lecture)
        #print(start_day_index , lecture_index)
        extra = lectures[(start_day_index + lecture_index-1) % len(lectures)].day.number - start_day
        if extra < 0:
            extra += 7
        x = 7 * number_of_weeks + extra
        date = subject.start_dates[squad_index] + timedelta(x)
        #print(material.number, date, 'weeks', number_of_weeks, 'extra', extra)
        return date
    else:
        return '_'

@register.filter
def get_my_date(material, profile):
    if type(material) is str:
        return '_'
    lectures = profile.hislectures.filter(subject = material.subject)
    if len(lectures) > 0:
        last_week_days = material.number % len(lectures)
        number_of_weeks = int(material.number/len(lectures))
        if last_week_days == 0:
            number_of_weeks -= 1
            last_week_days = len(lectures)
        x = 7 * number_of_weeks + last_week_days
        date = material.subject.start_date + timedelta(x)
        return date
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
    if num_of_lectures > 0 and  timezone.now().date() > subject.start_date:
        delta = (timezone.now().date() - subject.start_date).days
        number_of_weeks = int(delta / 7)
        finish = delta % 7
        start = int(subject.start_date.strftime('%w'))
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
def get_current_attendance(subject, squad):
    if not subject or not squad:
        return '_'
    lectures = squad.squad_lectures.filter(subject = subject)
    num_of_lectures = len(lectures)
    if num_of_lectures > 0 and  timezone.now().date() > subject.start_date:
        delta = (timezone.now().date() - subject.start_date).days
        number_of_weeks = int(delta / 7)
        finish = delta % 7
        start = int(subject.start_date.strftime('%w'))
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
        while material_number - i > 0:
            if counter == 4:
                break
            sm = subject.materials.filter(number = material_number - i)
            if len(sm) > 0:
                if len(sm[0].sm_atts.filter(squad = squad)) < len(squad.students.all()):
                    create_atts(squad, sm[0], subject)
                res = [sm[0].sm_atts.filter(squad = squad)] + res
                counter += 1
            i += 1
        if counter < 4:
            print('ho')
            i = 1
            while counter < 4 and i < 10:
                sm = subject.materials.filter(number = material_number + i)
                if len(sm) > 0:
                    if len(sm[0].sm_atts.filter(squad = squad)) < len(squad.students.all()):
                        create_atts(squad, sm[0], subject)
                    res.append(sm[0].sm_atts.filter(squad = squad))
                    counter += 1
                i += 1
        return res
    return '_'

@register.filter
def get_current_attendance_student(subject, profile):
    if not subject or not profile:
        return '_'
    lectures = profile.hislectures.filter(subject = subject)
    num_of_lectures = len(lectures)
    if num_of_lectures > 0 and  timezone.now().date() > subject.start_date:
        delta = (timezone.now().date() - subject.start_date).days
        number_of_weeks = int(delta / 7)
        finish = delta % 7
        start = int(subject.start_date.strftime('%w'))
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
        while material_number - i > 0:
            if counter == 4:
                break
            sm = subject.materials.filter(number = material_number - i)
            if len(sm) > 0:
                if len(sm[0].sm_atts.filter(student = profile)) < 1:
                    create_atts_student(sm[0], profile)
                res = [sm[0].sm_atts.filter(student = profile)] + res
                counter += 1
            i += 1
        if counter < 4:
            print('ho')
            i = 1
            while counter < 4 and i < 10:
                sm = subject.materials.filter(number = material_number + i)
                if len(sm) > 0:
                    if len(sm[0].sm_atts.filter(student = profile)) < 1:
                        create_atts_student(sm[0], profile)
                    res.append(sm[0].sm_atts.filter(student = profile))
                    counter += 1
                i += 1
        return res
    return '_'

def create_atts(squad, subject_materials, subject):
    for student in squad.students.all():
        if len(subject_materials.sm_atts.filter(student=student)) == 0:
            Attendance.objects.create(
                subject_materials = subject_materials,
                school=subject.school,
                teacher=subject.teacher.first(), 
                student=student,
                subject=subject,
                squad=squad
            )

def create_atts_student(subject_materials, student):
    Attendance.objects.create(
        subject_materials = subject_materials,
        school=subject_materials.school,
        teacher=subject_materials.subject.teacher.first(), 
        student=student,
        subject=subject_materials.subject,
        squad=student.hiscache.squad,
    )

