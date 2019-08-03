from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify
from markdown_deux import markdown

from django.utils.safestring import mark_safe
from transliterate import translit, get_available_language_codes
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from pagedown.widgets import PagedownWidget
from django.contrib.postgres.fields import ArrayField
from schools.models import *
import datetime

def upload_location(instance, filename):
    ProfileModel = instance.__class__
    if ProfileModel.objects.order_by("id").last():
        new_id = ProfileModel.objects.order_by("id").last().id + 1
    return "%s" %(filename)

class Profession(models.Model):
    title = models.TextField(blank = True,null = True,default='')
    class Meta:
        ordering = ['title']
class JobCategory(models.Model):
    title = models.TextField(blank = True,null = True,default='')
    salary = models.IntegerField(default=0)
    profession = models.ForeignKey(Profession, default=1, on_delete = models.CASCADE, related_name='job_categories') 
    class Meta:
        ordering = ['title']
class Skill(models.Model):
    confirmed = models.BooleanField(default=False)    
    confirmation_code = models.CharField(default='', max_length=250)
    confirmation_time = models.DateTimeField(auto_now_add=False, default=datetime.datetime.strptime('2000-01-01', "%Y-%m-%d"))
    tag_ids = ArrayField(models.IntegerField(), default = list)
    easy_skills = ArrayField(models.IntegerField(), default = list)
    middle_skills = ArrayField(models.IntegerField(), default = list)
    hard_skills = ArrayField(models.IntegerField(), default = list)
    pro_skills = ArrayField(models.IntegerField(), default = list)
    crm_show_free_cards = models.BooleanField(default=True)
    need_actions = models.IntegerField(default=0)
    crm_subject = models.ForeignKey(SubjectCategory, null=True, on_delete = models.CASCADE, related_name='choosed_by') 
    crm_age = models.ForeignKey(SubjectAge, null=True, on_delete = models.CASCADE, related_name='choosed_by') 
    crm_office = models.ForeignKey(Office, null=True, on_delete = models.CASCADE, related_name='choosed_by') 
    crm_subject2 = models.ForeignKey(SubjectCategory, null=True, on_delete = models.CASCADE, related_name='choosed_by2') 
    crm_age2 = models.ForeignKey(SubjectAge, null=True, on_delete = models.CASCADE, related_name='choosed_by2') 
    crm_office2 = models.ForeignKey(Office, null=True, on_delete = models.CASCADE, related_name='choosed_by2') 
    notifications_number = models.IntegerField(default=0)
    hint_numbers = ArrayField(models.IntegerField(), default = [0,0,0,0,0,0,0])
    birthdate = models.DateField(null = True, blank = True) 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.TextField(blank = True,null = True,default='name')

    schools = models.ManyToManyField(School, related_name='people')
    profession = models.ManyToManyField(Profession, related_name='workers')
    job_categories = models.ManyToManyField(JobCategory, related_name='job_workers')
    money = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)
    is_student = models.BooleanField(default=True)

    coins = models.IntegerField(default=0)
    mail = models.TextField(default = '')
    phone = models.TextField(blank = True,null = True, default = '')
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field",)
    height_field = models.IntegerField(default=0, null = True)
    width_field = models.IntegerField(default=0, null = True)

    crm_subject_connect = models.ManyToManyField(SubjectCategory, default=1, related_name='students')
    crm_age_connect = models.ManyToManyField(SubjectAge, default=1, related_name='students')
    skill = models.ForeignKey(Skill, null=True, on_delete = models.CASCADE, related_name='profile') 

    class Meta:
        ordering = ['-coins', 'first_name']

    def get_absolute_url(self):
        self.user.username = self.user.username.replace(' ', '_')
        self.user.username = self.user.username.replace('Қ', 'К')
        self.user.username = self.user.username.replace('қ', 'к')
        return reverse("accounts:profile", kwargs={"user": self.user})

    # APIs
    def subject_attendance(self):
        return reverse("accounts:subject_attendance")
    def squad_attendance(self):
        return reverse("accounts:squad_attendance")
    def more_attendance(self):
        return reverse("accounts:more_attendance")
    def more_attendance_student(self):
        return reverse("accounts:more_attendance_student")    
    def hislessons(self):
        return reverse("main:hislessons")        
    def get_api_change_url(self):
        return reverse("accounts:change-api-toggle")
    def city_api_url(self):
        return reverse("main:city_api_url")
    def filial_api_url(self):
        return reverse("main:filial_api_url")
    def subject_api_url(self):
        return reverse("main:subject_api_url")
    def tell_about_corruption(self):
        return reverse("accounts:tell_about_corruption")
    def change_url(self):
        return reverse("accounts:change_url")
    def update_schedule_url(self):
        return reverse("accounts:update_schedule_url")
    def miss_lecture_url(self):
        return reverse("accounts:miss_lecture_url")
    def attendance_change_url(self):
        return reverse("accounts:change_att_url")
    def attendance_present_url(self):
        return reverse("accounts:present_url")    
    def hint_url(self):
        return reverse("accounts:hint_url")    
    def update_hints(self):
        return reverse("accounts:update_hints")
    def get_notifications(self):
        return reverse('main:get_notifications')
    def make_payment(self):
        return reverse('accounts:make_payment')
    # Actions with lessons
    def create_folder_url(self):
        return reverse("library:create_folder_url")
    def create_lesson_url(self):
        return reverse("papers:create_lesson_url")
    def create_course_url(self):
        return reverse("papers:create_course_url")
    def file_action_url(self):
        return reverse("library:file_action_url")
    def paste_object_url(self):
        return reverse("library:paste_object_url")
    #Actions with documents
    def create_docfolder_url(self):
        return reverse("documents:create_docfolder_url")
    def docfile_action_url(self):
        return reverse("documents:docfile_action_url")
    def paste_docobject_url(self):
        return reverse("documents:paste_docobject_url")
    # Actions with news
    def create_post_url(self):
        return reverse("news:create_post_url")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class PaymentHistory(models.Model):
    school = models.ForeignKey(School, default=1, on_delete = models.CASCADE, related_name='payment_history') 
    user = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='payment_history') 
    manager = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='made_payments') 
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']

def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

class MissLesson(models.Model):
    profile = models.OneToOneField(Profile, null=True, on_delete = models.CASCADE) 
    text = models.TextField(blank = True,null = True,default='')
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field",)
    height_field = models.IntegerField(default=0, null = True)
    width_field = models.IntegerField(default=0, null = True)
    dates = ArrayField(models.DateField(null = True, blank = True), default = list)

class CRMColumn(models.Model):
    title = models.CharField(max_length=250)
    schools = models.ManyToManyField(School, related_name='crm_columns')
    class Meta:
        ordering = ['id']

class Hashtag(models.Model):
    title = models.CharField(max_length=250)
    schools = models.ManyToManyField(School, related_name='hashtags')
    class Meta:
        ordering = ['-id']

class CRMCard(models.Model):
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='card_author')
    card_user = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='card')
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='crm_cards')
    column = models.ForeignKey(CRMColumn, null=True, on_delete = models.CASCADE, related_name='cards')
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    mail = models.CharField(max_length=250)
    comments = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    saved = models.BooleanField(default=False)
    was_called = models.BooleanField(default=False)
    last_groups = models.IntegerField(default=-1)
    days_of_weeks = ArrayField(models.BooleanField(), default = list)
    action = models.CharField(max_length=250, default='')
    hashtags = models.ManyToManyField(Hashtag, related_name='cards')
    hashtag_ids = ArrayField(models.IntegerField(null=True), default=list)
    hashtag_numbers = ArrayField(models.IntegerField(null=True), default=list)
    class Meta:
        ordering = ['saved', '-timestamp']
    def call_helper(self):
        return reverse("schools:call_helper")
    def change_day_of_week(self):
        return reverse("schools:change_day_of_week")
    def take_url(self):
        return reverse("schools:take_url")

class CRMCardHistory(models.Model):
    action_author = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='card_histories')
    card = models.ForeignKey(CRMCard, null=True, on_delete = models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True)
    oldcolumn = models.CharField(max_length=250)
    newcolumn = models.CharField(max_length=250)
    edit = models.TextField(default='')
    class Meta:
        ordering = ['-timestamp']

class Notification(models.Model):
    text = models.TextField(default='')
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='made_notifications')
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='notifications')
    itstype = models.CharField(max_length=25)
    profession = models.ManyToManyField(Profession, related_name='notifications')
    url = models.TextField(default='', null=True)
    image_url = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']

class Review(models.Model):
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='reviews') 
    text = models.CharField(max_length=400)
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='reviews')
    to_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='to_reviews')
    rating = models.IntegerField(default=0, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']
