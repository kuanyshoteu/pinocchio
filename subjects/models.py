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

from accounts.models import Profile
from squads.models import Squad, SquadWeek
from papers.models import Lesson

def upload_location(instance, filename):
    CourseModel = instance.__class__
    if CourseModel.objects.order_by("id").last():
        new_id = CourseModel.objects.order_by("id").last().id + 1
    else:
        new_id=0
    return "%s/%s" %(instance.id, filename)

class Day(models.Model):
    title = models.TextField(default = '')
    number = models.IntegerField(default=0)
    class Meta:
        ordering = ['number']

class TimePeriod(models.Model):
    start = models.TextField(default = '')
    end = models.TextField(default = '')
    num =  models.IntegerField(default = 0)
    class Meta:
        ordering = ['num']

class Cell(models.Model):
    day = models.ForeignKey(Day, null=True, on_delete = models.CASCADE, related_name='day_cell')
    time_period = models.ForeignKey(TimePeriod, null=True, on_delete = models.CASCADE, related_name='time_cell')
    class Meta:
        ordering = ['day','time_period']

class Subject(models.Model):
    teacher = models.ManyToManyField(Profile, related_name='teachers_subjects')
    students = models.ManyToManyField(Profile, related_name='hissubjects')
    squads = models.ManyToManyField(Squad, related_name='subjects')

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image_icon = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    cabinet = models.TextField(default='')

    image_banner = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            width_field="width_field2", 
            height_field="height_field2")
    height_field2 = models.IntegerField(default=0, null=True)
    width_field2 = models.IntegerField(default=0, null=True)

    image_back = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            width_field="width_field3", 
            height_field="height_field3")
    height_field3 = models.IntegerField(default=0, null=True)
    width_field3 = models.IntegerField(default=0, null=True)
    color_back = models.TextField(default='')

    content = models.TextField()
    slogan = models.CharField(max_length=250, default='')    
    
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)

    number_of_lectures = models.IntegerField(default = 0)

    class Meta:
        ordering = ['id']
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        return reverse("subjects:detail", kwargs={"slug": self.slug})
    def get_delete_url(self):
        return reverse("subjects:delete", kwargs={"slug": self.slug})
    def get_update_url(self):
        return reverse("subjects:update", kwargs={"slug": self.slug})
    def get_list_url(self):
        return reverse("subjects:list")
    def videos_url(self):
        return reverse("subjects:videos_url", kwargs={"slug": self.slug})
    def lessons_url(self):
        return reverse("subjects:lessons_url", kwargs={"slug": self.slug})
    def set_time_url(self):
        return reverse("subjects:set_time_url")
    def get_markdown(self):
        return mark_safe(markdown(self.content))
    def change_schedule_url(self):
        return reverse("subjects:change_schedule_url", kwargs={"id": self.id})
    def delete_squad_url(self):
        return reverse("subjects:delete_squad_url")

    def subject_schedule_url(self):
        return reverse("subjects:subject_schedule_url",kwargs={"id": self.id})
    def squad_list_url(self):
        return reverse("subjects:squad_list",kwargs={"id": self.id})
    
        
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    def add_paper_url(self):
        return reverse("subjects:add_paper_url")        
    def add_squad_url(self):
        return reverse("subjects:add_squad_url")   
    def change_teacher_url(self):
        return reverse("subjects:change_teacher_url")  
    def change_start_url(self):
        return reverse("subjects:change_start_url")  
    def change_end_url(self):
        return reverse("subjects:change_end_url")       

def create_slug(instance, new_slug=None):
    if len(Subject.objects.all()) > 0:
        subject = Subject.objects.all()[len(Subject.objects.all())-1]
        slug = slugify('qqq' + str(subject.id + 1))
        if len(Subject.objects.filter(slug=slug)) > 0:
            slug = slugify('qqq' + str(subject.id + 1) + 'q')
    else:
        slug = slugify('0')
    return slug 

def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_course_receiver, sender=Subject)

class SubjectMaterials(models.Model):
    subject = models.ForeignKey(Subject,null=True, on_delete = models.CASCADE, related_name='materials')
    lessons = models.ManyToManyField(Lesson, related_name='subject_materials')
    number = models.IntegerField(default=0)
    done_by = models.ManyToManyField(Profile, related_name='done_subject_materials')
    class Meta:
        ordering = ['number']
    def remove_lesson(self):
        return reverse("subjects:remove_lesson")

class SquadCell(models.Model):
    squad = models.ForeignKey(Squad, null=True, on_delete = models.CASCADE, related_name='cells')
    subject_materials = models.ManyToManyField(SubjectMaterials, related_name='material_cells')
    week = models.ForeignKey(SquadWeek, null=True, on_delete = models.CASCADE, related_name='week_cells')
    date = models.DateField(auto_now_add=False)
    cell = models.ForeignKey(Cell, null=True, on_delete = models.CASCADE, related_name='cell_squad_cells')
    time_period = models.ForeignKey(TimePeriod, null=True, on_delete = models.CASCADE, related_name='squad_cells')
    class Meta:
        ordering = ['date', 'time_period']

class Lecture(models.Model):
    cell = models.ForeignKey(Cell, null=True, on_delete = models.CASCADE, related_name='lectures')
    subject = models.ForeignKey(Subject, null=True, on_delete = models.CASCADE, related_name='subject_lectures')
    squad = models.ForeignKey(Squad, null=True, on_delete = models.CASCADE, related_name='squad_lectures')
    class Meta:
        ordering = ['cell']

class Attendance(models.Model):
    teacher = models.ForeignKey(Profile, default=119, on_delete = models.CASCADE, related_name='madegrades')
    student = models.ForeignKey(Profile, default=1, on_delete = models.CASCADE, related_name='hisgrades')
    squad_cell = models.ForeignKey(SquadCell, null=True, on_delete = models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject,null=True, on_delete = models.CASCADE, related_name='subject_attendances')
    squad = models.ForeignKey(Squad,null=True, on_delete = models.CASCADE, related_name='squad_attendances')
    subject_materials = models.ForeignKey(SubjectMaterials,null=True, on_delete = models.CASCADE, related_name='sm_atts')

    present = models.TextField(default = '')
    grade = models.IntegerField(default = -1)
    class Meta:
        ordering = ['subject', 'squad', 'squad_cell', 'student']
    def change_url(self):
        return reverse("accounts:change_att_url")
    def present_url(self):
        return reverse("accounts:present_url")

class SubjectCategory(models.Model):
    title = models.TextField(default = '')
    subjects = models.ManyToManyField(Subject, related_name='subject_categories')
