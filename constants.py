from accounts.models import *
from subjects.models import *
from schools.models import School
from django.http import HttpResponse, HttpResponseRedirect, Http404
import string
import random

def random_password():
    symbols = string.ascii_letters + string.digits
    password = ''
    for i in range(0, 9):
        password += random.choice(symbols)
def get_profile(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
    else:
        raise Http404
    return profile

def only_teachers(profile):
    profession = Profession.objects.get(title = 'Teacher')
    profession2 = Profession.objects.get(title = 'Director')
    print(profession ,profile.profession.all(), profession in profile.profession.all())
    if not profession in profile.profession.all() and not profession2 in profile.profession.all():
        raise Http404

def only_managers(profile):
    profession = Profession.objects.get(title = 'Manager')
    profession2 = Profession.objects.get(title = 'Director')
    if not profession in profile.profession.all() and not profession2 in profile.profession.all():
        raise Http404

def only_directors(profile):
    profession = Profession.objects.get(title = 'Director')
    if not profession in profile.profession.all():
        raise Http404

def only_staff(profile):
    manager = Profession.objects.get(title = 'Manager')
    teacher = Profession.objects.get(title = 'Teacher')
    director = Profession.objects.get(title = 'Director')
    if manager in profile.profession.all() or teacher in profile.profession.all() or director in profile.profession.all():
        pass
    else:
        raise Http404

def is_profi(profile, job_name):
    profession = Profession.objects.get(title = job_name)
    director = Profession.objects.get(title = 'Director')
    if job_name != 'Director' and director in profile.profession.all():
    	if not profile.is_student:
    		return True
    return profession in profile.profession.all()

def check_cells():
    time_periods = TimePeriod.objects.all()
    days = Day.objects.all()
    cells = Cell.objects.all()
    if len(cells) < len(days) * len(time_periods):
        for day in days:
            for timep in time_periods:
                new_cell = Cell.objects.get_or_create(day = day, time_period = timep)

def all_into_first_school():
    school = School.objects.all()[0]
    for p in Profile.objects.all():
        p.school = school
        p.save()

def register_by_file():
    ff = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file = str(ff) + "/abc.xlsx"
    data = pd.read_excel(file,header=None) #reading file
    a = data.values.tolist()
    for row in a:
        new_id = User.objects.using('akuir').order_by("id").last().id + 1
        user = User.objects.create(username='user' + str(new_id), password=str(row[1]))
        profile = Profile.objects.get(user = user)
        profile.first_name = row[0]
        profile.phone = str(row[2])
        profile.save()

def all_teachers(school):
    res = []
    profession = Profession.objects.get(title = 'Teacher')
    for h in school.people.all():
        if h in profession.workers.all():
            res.append(h)
    return res
