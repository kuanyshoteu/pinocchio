from accounts.models import *
from subjects.models import *
from schools.models import School
from django.http import HttpResponse, HttpResponseRedirect, Http404

def get_profile(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
    else:
        raise Http404
    return profile

def is_profi(profile, job_name):
    profession = Profession.objects.get(title = job_name)
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
