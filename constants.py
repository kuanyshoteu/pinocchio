from accounts.models import *
from subjects.models import *
from schools.models import School
from django.http import HttpResponse, HttpResponseRedirect, Http404
import string
import random
from django.core.mail import send_mail
import requests
from django.core.mail import EmailMultiAlternatives

def send_sms(phones, message, time):
    login = 'Pinocchio'
    password = 'Siski11zhopa'
    url = 'https://smsc.kz/sys/send.php?login='+login+'&psw='+password+'&phones='+phones+'&mes='+message+'&time='+time+'&sender=Pinocchiokz'
    requests.post(url)

def send_hello_email(profile, password, timeaddress):
    text = "Здравствуйте "+profile.first_name+ "! Вас зарегестрировали на сайте <a href='pinocchio.kz'>Pinocchio.kz</a><br><br>"+timeaddress+". Расписание можете посмотреть в личной странице"
    login_text="<br>Ваш логин: "+profile.phone+" или "+profile.mail
    password_text = "<br>Ваш пароль (не говорите никому): "+password
    html_content = text+login_text+password_text+" <br><br>С уважением, команда <a href='pinocchio.kz'>Pinocchio.kz</a>"

    msg = EmailMultiAlternatives("Добро пожаловать на Pinocchio.kz", 'q', 'aaa.academy.kz@gmail.com', [profile.mail])
    msg.attach_alternative(html_content, "text/html")
    print(msg)
    msg.send()

def send_email(subject, html_content, send_to):
    print(subject, html_content, send_to)
    msg = EmailMultiAlternatives(subject, 'qq', 'aaa.academy.kz@gmail.com', send_to)
    msg.attach_alternative(html_content, "text/html")
    print(msg)
    msg.send()

def random_password():
    symbols = string.ascii_letters + string.digits
    password = ''
    for i in range(0, 9):
        password += random.choice(symbols)
    return password

def random_secrete_confirm():
    symbols = string.ascii_letters + string.digits
    password = ''
    for i in range(0, 20):
        password += random.choice(symbols)
    return password

def get_profile(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
    else:
        raise Http404
    return profile

def is_in_school(profile, school):
    if not school in profile.schools.all():
        raise Http404

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
    if job_name != 'Teacher' and director in profile.profession.all():
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
    profession = Profession.objects.get(title = 'Teacher')
    return profession.workers.filter(schools=school)

