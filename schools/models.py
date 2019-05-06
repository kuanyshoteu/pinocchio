from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from markdown_deux import markdown
from django.utils.safestring import mark_safe
from transliterate import translit, get_available_language_codes
from django.contrib.postgres.fields import ArrayField, HStoreField


def upload_location(instance, filename):
    CourseModel = instance.__class__
    if CourseModel.objects.order_by("id").last():
        new_id = CourseModel.objects.order_by("id").last().id + 1
    else:
        new_id=0
    return "%s/%s" %(instance.id, filename)

class School(models.Model):
    title = models.CharField(max_length=250)
    official_school = models.BooleanField(default = False)
    image_icon = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)

    image_banner = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            width_field="width_field2", 
            height_field="height_field2")
    height_field2 = models.IntegerField(default=0, null=True)
    width_field2 = models.IntegerField(default=0, null=True)
    
    content = models.TextField(default='')
    slogan = models.CharField(max_length=250, default='')

    new_schedule = models.BooleanField(default = False)

    class Meta:
        ordering = ['title']
    def __unicode__(self):
        return self.title
    # School information pages
    def get_absolute_url(self):
        return reverse("schools:info")
    def get_requests_url(self):
        return reverse("schools:requests")
    def get_recalls_url(self):
        return reverse("schools:recalls")
    def get_teachers_url(self):
        return reverse("schools:teachers")
    def get_crm_url(self):
        return reverse("schools:crm")
    def get_students_url(self):
        return reverse("schools:students")
    def get_courses_url(self):
        return reverse("schools:courses")
    def move_card_url(self):
        return reverse("schools:move_card_url")
    def get_markdown(self):
        return mark_safe(markdown(self.content))
    # API Registration 
    def register_to_school(self):
        return reverse("schools:register_to_school")
    def edit_card_url(self):
        return reverse("schools:edit_card_url")
    def add_card_url(self):
        return reverse("schools:add_card_url")
    def save_card_as_user(self):
        return reverse("schools:save_card_as_user")
    def salary_url(self):
        return reverse("schools:salary_url")
    def save_job_salary(self):
        return reverse("schools:save_job_salary")
    def delete_card_url(self):
        return reverse("schools:delete_card_url")
    # School objects
    def get_school_documents(self):
        return reverse("documents:get_school_documents", kwargs={"school_id": self.id})
    def get_school_library(self):
        return reverse("library:get_school_library", kwargs={"school_id": self.id})
    def get_school_posts(self):
        return reverse("news:get_school_posts", kwargs={"school_id": self.id})
    def get_school_squads(self):
        return reverse("squads:get_school_squads", kwargs={"school_id": self.id})
    def get_school_subjects(self):
        return reverse("subjects:get_school_subjects", kwargs={"school_id": self.id})
    def get_school_ratings(self):
        return reverse("schools:get_school_ratings", kwargs={"school_id": self.id})
    def get_school_todolists(self):
        return reverse("todolist:get_school_todolists", kwargs={"school_id": self.id})
    def crm_option_url(self):
        return reverse("schools:crm_option_url")

class SubjectCategory(models.Model):
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='school_subject_categories') 
    title = models.CharField(max_length=250)

class SubjectAge(models.Model):
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='school_subject_ages')
    title = models.CharField(max_length=250)

class Office(models.Model):
    title = models.CharField(max_length=250)
    address = models.TextField(default='')
    capacity = models.IntegerField(default=0)
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='school_offices')

class Cabinet(models.Model):
    title = models.CharField(max_length=250)
    capacity = models.IntegerField(default=0)
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='school_cabinets')

