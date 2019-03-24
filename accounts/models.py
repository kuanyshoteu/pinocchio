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

def upload_location(instance, filename):
    ProfileModel = instance.__class__
    if ProfileModel.objects.order_by("id").last():
        new_id = ProfileModel.objects.order_by("id").last().id + 1
    return "%s" %(filename)

class Profession(models.Model):
    title = models.TextField(blank = True,null = True,default='')
class JobCategory(models.Model):
    title = models.TextField(blank = True,null = True,default='')
    salary = models.IntegerField(default=0)
    profession = models.ForeignKey(Profession, default=1, on_delete = models.CASCADE, related_name='job_categories') 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.TextField(blank = True,null = True,default='')

    schools = models.ManyToManyField(School, related_name='people')
    profession = models.ManyToManyField(Profession, related_name='workers')
    job_categories = models.ManyToManyField(JobCategory, related_name='job_workers')
    money = models.IntegerField(default=0)
    is_student = models.BooleanField(default=True)

    coins = models.IntegerField(default=0)
    birthdate = models.DateField(null = True, blank = True) 
    mail = models.TextField(default = '')
    phone = models.TextField(blank = True,null = True, default = '')
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field",)
    height_field = models.IntegerField(default=0, null = True)
    width_field = models.IntegerField(default=0, null = True)

    tag_ids = ArrayField(models.IntegerField(), default = list)
    easy_skills = ArrayField(models.IntegerField(), default = list)
    middle_skills = ArrayField(models.IntegerField(), default = list)
    hard_skills = ArrayField(models.IntegerField(), default = list)
    pro_skills = ArrayField(models.IntegerField(), default = list)

    crm_subject = models.ForeignKey(SubjectCategory, null=True, on_delete = models.CASCADE, related_name='choosed_by') 
    crm_age = models.ForeignKey(SubjectAge, null=True, on_delete = models.CASCADE, related_name='choosed_by') 
    crm_office = models.ForeignKey(Office, null=True, on_delete = models.CASCADE, related_name='choosed_by') 

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

class Zaiavka(models.Model):
    school = models.ForeignKey(School, default=1, on_delete = models.CASCADE, related_name='zaiavkas') 
    first_name = models.TextField()
    mail = models.TextField(default = '')
    phone = models.TextField(blank = True,null = True, default = '')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']
    
    def get_api_deletezaiavka_url(self):
        return reverse("accounts:deletezaiavka-api-toggle", kwargs={"id": self.id})        

def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

class Corruption(models.Model):
    text = models.TextField(default='')
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='his_messages')
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='corruptions')

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
