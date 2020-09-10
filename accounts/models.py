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
        ordering = ['-title']
class JobCategory(models.Model):
    title = models.TextField(blank = True,null = True,default='')
    salary = models.IntegerField(default=0)
    profession = models.ForeignKey(Profession, default=1, on_delete = models.CASCADE, related_name='job_categories') 
    schools = models.ManyToManyField(School, related_name='job_categories')
    class Meta:
        ordering = ['title']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE,related_name='profile')
    first_name = models.TextField(blank = True,null = True,default='name')
    schools = models.ManyToManyField(School, related_name='people')
    profession = models.ManyToManyField(Profession, related_name='workers')
    job_categories = models.ManyToManyField(JobCategory, related_name='job_workers')
    money = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)
    is_student = models.BooleanField(default=True)
    coins = models.IntegerField(default=0)
    mail = models.TextField(blank = True,default = '',null = True)
    phone = models.TextField(blank = True,null = True, default = '')
    extra_phone = models.TextField(blank = True,null = True, default = '')
    image = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            )
    confirmed = models.BooleanField(default=True)
    confirmation_code = models.CharField(default='', max_length=250)
    confirmation_time = models.DateTimeField(auto_now_add=False, default=datetime.datetime.strptime('2000-01-01', "%Y-%m-%d"))
    hint_numbers = ArrayField(models.IntegerField(), default = list)
    end_work = models.DateTimeField(auto_now_add=False, null=True)
    check_end_work = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_student', 'check_end_work', 'id']

    def get_absolute_url(self):
        self.user.username = self.user.username.replace(' ', '_')
        self.user.username = self.user.username.replace('Қ', 'К')
        self.user.username = self.user.username.replace('қ', 'к')
        return reverse("accounts:profile", kwargs={"user": self.user})

class Skill(models.Model):
    author = models.OneToOneField(Profile, null=True, on_delete = models.CASCADE, related_name='skill')
    tag_ids = ArrayField(models.IntegerField(), default = list)
    easy_skills = ArrayField(models.IntegerField(), default = list)
    middle_skills = ArrayField(models.IntegerField(), default = list)
    hard_skills = ArrayField(models.IntegerField(), default = list)
    pro_skills = ArrayField(models.IntegerField(), default = list)
    interested_subjects = models.ManyToManyField(SubjectCategory, default=1, related_name='interested_students')

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
    extra_phone = models.CharField(max_length=250, default="")
    mail = models.CharField(max_length=250)
    comments = models.CharField(max_length=250)
    parents = models.CharField(max_length=250, default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    saved = models.BooleanField(default=False)
    was_called = models.BooleanField(default=False)
    last_groups = models.IntegerField(default=-1)
    days_of_weeks = ArrayField(models.BooleanField(), default = list)
    hashtags = models.ManyToManyField(Hashtag, related_name='cards')
    premoney = models.IntegerField(default=0)
    color = models.CharField(max_length=250, default='white')
    social_media_id = models.CharField(max_length=50, default='')
    birthday = models.DateField(null = True, blank = True)
    class Meta:
        ordering = ['-timestamp']

class CardMail(models.Model):
    action_author = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='dialogs')
    text = models.TextField(blank = True,null = True,default='')
    card = models.ForeignKey(CRMCard, null=True, on_delete = models.CASCADE, related_name='mails')
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=250, default='')
    is_client = models.BooleanField(default=False)
    social_media = models.ForeignKey(SocialMediaAccount, null=True, on_delete = models.CASCADE, related_name='mails')
    class Meta:
        ordering = ['id']

class BigMail(models.Model):
    action_author = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='big_mails')
    text = models.TextField(blank = True,null = True,default='')
    card = models.ManyToManyField(CRMCard, related_name='big_mails')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['id']

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

class SchoolMoneyHistory(models.Model):
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='school_money_histories')
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='school_money_histories')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']