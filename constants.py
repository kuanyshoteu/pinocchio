from django.shortcuts import render, redirect
from accounts.models import *
from subjects.models import *
from schools.models import School
from django.http import HttpResponse, HttpResponseRedirect, Http404
import string
import random
from django.core.mail import send_mail
import requests
from django.core.mail import EmailMultiAlternatives

from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

cloudpayments_id = 'pk_8f05633d39130c02981943d45a4a4'
cloudpayments_secretkey = '933e77aa9d8497d3149d550f6e1e4873'

wazzup24_secretkey = '1b8dca4bc26b4b9098c169c3ecc1736d'

def send_sms(phones, message, time):
    login = 'Pinocchio'
    password = 'Siski11zhopa'
    url = 'https://smsc.kz/sys/send.php?login='+login+'&psw='+password+'&phones='+phones+'&mes='+message+'&time='+time#+'&sender=bilimtapkz'
    requests.post(url)

def send_email(subject, html_content, send_to):
    msg = EmailMultiAlternatives(subject, 'qq', 'aaa.academy.kz@gmail.com', send_to)
    ender = " <br><br>С уважением, команда <a href='bilimtap.kz'>bilimtap.kz</a>"
    msg.attach_alternative(html_content+ender, "text/html")
    msg.send()

def send_email_client(subject, html_content, send_to):
    msg = EmailMultiAlternatives(subject, 'qq', 'aaa.academy.kz@gmail.com', send_to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_hello_email(first_name, phone, mail, password, timeaddress):
    text = "Здравствуйте "+first_name+ "! Вас зарегестрировали на сайте <a href='bilimtap.kz'>bilimtap.kz</a><br><br>"+timeaddress+". Расписание можете посмотреть в личной странице"
    login_text="<br>Ваш логин: "+phone+" или "+mail
    password_text = "<br>Ваш пароль (не говорите никому): "+password
    ender = " <br><br>С уважением, команда <a href='bilimtap.kz'>bilimtap.kz</a>"
    html_content = text+login_text+password_text+ender
    msg = EmailMultiAlternatives("Добро пожаловать на bilimtap.kz", 'q', 'aaa.academy.kz@gmail.com', [mail])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def change_school_money(school, amount, reason, name):
    school.money += amount
    if reason == 'student_payment':
        school.money_object.create(title='Оплата за учебу ' + name, amount=amount)
    elif reason == 'teacher_salary':
        school.money_object.create(title='Зарплата ' + name, amount=amount)
    else:
        school.money_object.create(title=reason, amount=amount)
    now = timezone.now().date()
    spend = 0
    earn = 0
    if amount > 0:
        earn = amount
    else:
        spend = amount
    first_day = get_frist_day_of_month(now)
    if len(school.money_months.all()) == 0:
        create_money_month(school, first_day, spend, earn)
    last = school.money_months.last()
    if now - relativedelta(months=1) >= last.month:
        create_money_month(school, first_day, spend, earn)
        last = school.money_months.last()
    if amount > 0:
        last.money_earn[0] += amount
    else:
        if reason == 'teacher_salary':
            last.money_spend[0] += amount
        else:
            last.money_spend[1] += amount
    last.save()

def create_money_month(school, first_day, spend, earn):
    new_money_month = school.money_months.create(
        month = first_day,
        money_spend = [0, 0, 0, 0, 0],
        money_earn = [0, 0, 0, 0, 0],
    )
    new_money_month.save()

def get_frist_day_of_month(now):
    month = now.strftime('%m')
    year = now.strftime('%Y')
    first_day = datetime.datetime.strptime(year+'-'+month+'-01', "%Y-%m-%d").date()
    return first_day

def random_password():
    symbols = string.ascii_letters
    digits = string.digits
    password = ''
    for i in range(0, 4):
        password += random.choice(symbols)
    for i in range(0, 4):
        password += random.choice(digits)
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
    if is_profi(profile, 'Moderator'):
        return True
    if not school in profile.schools.all():
        raise Http404

def only_teachers(profile):
    profession = Profession.objects.get(title = 'Teacher')
    profession2 = Profession.objects.get(title = 'Director')
    if not profession in profile.profession.all() and not profession2 in profile.profession.all():
        raise Http404

def only_managers(profile):
    profession = Profession.objects.get(title = 'Manager')
    profession2 = Profession.objects.get(title = 'Director')
    if not profession in profile.profession.all() and not profession2 in profile.profession.all():
        raise Http404

def only_main_managers(profile):
    profession = Profession.objects.get(title = 'Director')
    if not profession in profile.profession.all():
        job = JobCategory.objects.filter(title='Менеджер стажер')
        if len(job) > 0:
            job = job[0]
            if job in profile.job_categories.all():
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
    moderator = Profession.objects.get(title = 'Moderator')
    if moderator in profile.profession.all():
        return True
    if job_name != 'Teacher' and job_name != 'Moderator' and director in profile.profession.all():
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

def is_moderator_school(request, profile):
    if request.GET.get('type'):
        if request.GET.get('type') == 'moderator':
            if is_profi(profile, 'Moderator') and request.GET.get('mod_school_id') != '':
                school = School.objects.get(id=int(request.GET.get('mod_school_id')))
                return school
    school = profile.schools.first()
    if school.version == 'business':
        if school.version_date + timedelta(30) < timezone.now():
            school.version = 'free'
            school.save()
    return school

def get_times(interval):
    res = []
    time = 480
    end = 22
    while time <= end * 60:
        hour = str(int(time/60))
        if len(hour) == 1:
            hour = '0' + hour
        minute = str(int(time%60))
        if len(minute) == 1:
            minute = '0' + minute
        res.append(hour + ":" + minute )
        time += interval
    return res

def get_days():
    res = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    return res

def get_day_text(text):
    res = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    return res.index(text)+1

def hidden_filter_ids():
    res = set()
    titles = ['IELTS', 'TOEFL', 'Математика', 'Логика', 'SAT', 'GRE', 'GMAT']
    for title in titles:
        sc = SubjectCategory.objects.filter(title=title)
        res = chain(sc, res)

    langs = SubjectCategory.objects.filter(title__icontains="язык")
    res = chain(langs, res)
    return set(res)

def get_card_data_by_column(card, column_id):
    res = []
    author_name = 'Свободная'
    author_url = ''
    author_id = -1
    if card.author_profile:
        author = card.author_profile
        author_name = author.first_name
        author_url = author.get_absolute_url()
        author_id = author.id
    arr = [
        card.id,                            # 0
        card.name,                          # 1
        card.phone,                         # 2
        card.color,                         # 3
        str(card.saved),                    # 4
        author_name,                        # 5
        author_url,                         # 6
        ]
    res.append(arr)
    return res

def get_card_form_by_column(card, column_id):
    res = []
    author_id = -1
    if card.author_profile:
        author_id = card.author_profile.id
    arr2 = [
        card.mail,                          # 0
        card.extra_phone,                   # 1
        card.parents,                       # 2
        card.comments,                      # 3
        author_id,                          # 4
        card.social_media_id,               # 5
        card.days_of_weeks,                 # 6
        card.birthday,                      # 7
    ]
    res.append(arr2)
    return res

def get_card_dialog(card):
    res = []
    query = card.mails.all()
    p = Paginator(query, 7)
    page1 = p.page(1)
    for mail in page1.object_list:
        action_author = ''
        if mail.action_author:
            action_author = mail.action_author.first_name
        elif mail.social_media:
            action_author = mail.social_media.username
        res.append([
            mail.id,
            action_author,
            mail.text,
            mail.method,
            mail.timestamp.strftime('%d %B %H:%M'),
            mail.is_client,
            ])
    return res

img_formats = ['jpg', 'jpeg', 'png']

def check_school_version(school, version):
    if school.version == version:
        if version == 'business':
            if school.version_date > timezone.now():
                return True
            else:
                school.version = 'free'
                school.save()
        else:
            return True
    else:
        return False
