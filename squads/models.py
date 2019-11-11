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
from django.contrib.postgres.fields import ArrayField, HStoreField

from accounts.models import Profile,CRMCard
from schools.models import *

def upload_location(instance, filename):
    CourseModel = instance.__class__
    if CourseModel.objects.order_by("id").last():
        new_id = CourseModel.objects.order_by("id").last().id + 1
    else:
        new_id=0
    return "%s/%s" %(instance.id, filename)

class Squad(models.Model):
    teacher = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='hissquads') 
    students = models.ManyToManyField(Profile, default=1, related_name='squads')
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='groups')
    office = models.ForeignKey(Office, null=True, on_delete = models.CASCADE, related_name='groups')
    age = models.ManyToManyField(SubjectAge, related_name='groups')
    level = models.ManyToManyField(SubjectLevel, related_name='groups')
    rating_choices = models.ManyToManyField(Profile, related_name='rating_squad_choice')

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image_icon = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            )
    image_banner = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            )    
    content = models.TextField(default='')
    slogan = models.CharField(max_length=250, default='')

    start_date = models.DateField(auto_now_add=False)
    start_day = models.IntegerField(default=0)
    color_back = models.TextField(default='')
    shown = models.BooleanField(default=True)
    deleted_time = models.DateTimeField(auto_now_add=True)        

    class Meta:
        ordering = ['title']
    def __unicode__(self):
        return self.title
    def ___str__(self):
        return self.title
    def get_absolute_url(self):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        return reverse("squads:detail", kwargs={"slug": self.slug})
    def get_delete_url(self):
        return reverse("squads:delete", kwargs={"slug": self.slug})
    def get_update_url(self):
        return reverse("squads:update", kwargs={"slug": self.slug})
    def get_list_url(self):
        return reverse("squads:list")
    def videos_url(self):
        return reverse("squads:videos_url", kwargs={"slug": self.slug})
    def lessons_url(self):
        return reverse("squads:lessons_url", kwargs={"slug": self.slug})
    def set_time_url(self):
        return reverse("squads:set_time_url")
    def get_markdown(self):
        return mark_safe(markdown(self.content))
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    def calendar_url(self):
        return reverse("squads:calendar_url")        
    def add_paper_url(self):
        return reverse("squads:add_paper_url")   
    def change_curator_url(self):
        return reverse("squads:change_curator_url")    
    def add_student_url(self):
        return reverse("squads:add_student_url")   
    def change_office(self):
        return reverse("squads:change_office",kwargs={"id": self.id})     
    def choose_color(self):
        return reverse("squads:choose_color",kwargs={"id": self.id})     

    def change_schedule_url(self):
        return reverse("squads:change_schedule_url", kwargs={"id": self.id})
    def delete_subject_url(self):
        return reverse("squads:delete_subject_url")
    def squad_schedule_url(self):
        return reverse("squads:squad_schedule_url",kwargs={"id": self.id})
    def subject_list_url(self):
        return reverse("squads:subject_list",kwargs={"id": self.id})    
    def add_subject_url(self):
        return reverse("squads:add_subject_url")   
    def delete_lesson_url(self):
        return reverse("squads:delete_lesson_url",kwargs={"id": self.id})       
    def change_lecture_cabinet(self):
        return reverse("squads:change_lecture_cabinet")
    def get_page_students(self):
        return reverse("squads:get_page_students",kwargs={"id": self.id})
    def hint_students_group(self):
        return reverse("squads:hint_students_group",kwargs={"id": self.id})
    def const_create_lectures(self):
        return reverse("squads:const_create_lectures",kwargs={"id": self.id})        

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if not slug:
        slug = slugify(translit(instance.title, 'ru', reversed=True))
    if new_slug is not None:
        slug = new_slug
    qs = Squad.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_course_receiver, sender=Squad)

class Bug(models.Model):
    text = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)

class SquadHistory(models.Model):
    squad = models.ForeignKey(Squad,null=True,on_delete = models.CASCADE,related_name='squad_histories')
    action_author = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='squad_histories')
    timestamp = models.DateTimeField(auto_now_add=True)
    edit = models.TextField(default='')
    class Meta:
        ordering = ['-timestamp']

class PaymentHistory(models.Model):
    school = models.ForeignKey(School, default=1, on_delete = models.CASCADE, related_name='payment_history') 
    user = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='payment_history') 
    squad = models.ForeignKey(Squad,null=True,on_delete = models.CASCADE,related_name='payment_history')
    action_author = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='made_payments') 
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']

class DiscountSchool(models.Model):
    title = models.CharField(max_length=250)
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='discounts') 
    amount = models.IntegerField(default=0)
    discount_type = models.CharField(max_length=250, default='') #percent or tenge
    class Meta:
        ordering = ['id']
    def create_url(self):
        return reverse("schools:discount_create_url")
    def delete_url(self):
        return reverse("schools:discount_delete_url")

class NeedMoney(models.Model):
    squad = models.ForeignKey(Squad,null=True,on_delete = models.CASCADE,related_name='need_money')
    card = models.ForeignKey(CRMCard,null=True,on_delete = models.CASCADE,related_name='need_money')
    money = models.IntegerField(default=0)
    lesson_bill = models.IntegerField(default=0)
    bill = models.IntegerField(default=0)
    course_bill = models.IntegerField(default=0)
    discount_school = models.ManyToManyField(DiscountSchool, related_name='nms')
