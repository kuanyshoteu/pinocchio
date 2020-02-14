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
    image_icon = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            )
    content = models.TextField(default='')
    slogan = models.CharField(max_length=250, default='')
    site = models.CharField(max_length=250, default='')
    worktime = models.CharField(max_length=250, default='')
    phones = ArrayField(models.TextField(), default = list)
    social_networks = ArrayField(models.TextField(), default = list)
    social_network_links = ArrayField(models.TextField(), default = list)
    offices = models.IntegerField(default=0)
    average_cost = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    money = models.IntegerField(default=0)
    money_update_person = models.CharField(max_length=50, default='')
    money_update_date = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=10, default='')
    sms_amount = models.IntegerField(default=0)
    pay_day_diff = models.IntegerField(default=5)
    schedule_type = models.CharField(max_length=10, default='classic') #May be "classic" or "new"
    schedule_interval = models.IntegerField(default=60)

    class Meta:
        ordering = ['version','rating', '-average_cost']
    def __unicode__(self):
        return self.title
    def ___str__(self):
        return self.title    
    def landing(self):
        return reverse("schools:landing", kwargs={"school_id": self.id})
    # Edit API's
    def create_school(self):
        return reverse("main:create_school")
    def change_title_url(self):
        return reverse("schools:change_title_url")
    def change_slogan_url(self):
        return reverse("schools:change_slogan_url")
    def change_content_url(self):
        return reverse("schools:change_content_url")
    def change_site_url(self):
        return reverse("schools:change_site_url")    
    # School information pages
    def get_absolute_url(self):
        return reverse("schools:info")
    def school_moderator_url(self):
        return reverse("schools:info_moderator", kwargs={"school_id": self.id})
    def get_requests_url(self):
        return reverse("schools:requests")
    def get_recalls_url(self):
        return reverse("schools:recalls")
    def get_salaries_url(self):
        return reverse("schools:salaries")
    def get_payments_url(self):
        return reverse("schools:payments")
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
    def get_card_squads(self):
        return reverse("schools:get_card_squads")
    def update_voronka(self):
        return reverse("schools:update_voronka")
    def new_money_object(self):
        return reverse("schools:new_money_object")
    def show_money_history(self):
        return reverse("schools:show_money_history")
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
    def get_school_report(self):
        return reverse("schools:get_school_report", kwargs={"school_id": self.id})
    def crm_option_url(self):
        return reverse("schools:crm_option_url")
    def crm_option_url2(self):
        return reverse("schools:crm_option_url2")
    def open_card_url(self):
        return reverse("schools:open_card_url")
    def show_free_cards(self):
        return reverse("schools:show_free_cards", kwargs={"school_id": self.id})
    # School map
    def get_landing(self):
        return reverse("schools:get_landing")
    def save_review_url(self):
        return reverse("schools:save_review_url", kwargs={"school_id": self.id})
    def make_zaiavka(self):
        return reverse("schools:make_zaiavka", kwargs={"school_id": self.id})
    def create_social_url(self):
        return reverse("schools:create_social_url")
    def delete_social_url(self):
        return reverse("schools:delete_social_url")
    def predoplata(self):
        return reverse("schools:predoplata")

class SchoolBanner(models.Model):
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='banners')
    image_banner = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            )
    class Meta:
        ordering = ['id']
    def delete_school_banner(self):
        return reverse("schools:delete_school_banner")


class SchoolFilter(models.Model):
    title = models.CharField(max_length=250)
    def delete_url(self):
        return reverse("schools:age_delete_url")
    def create_url(self):
        return reverse("schools:age_create_url")
    def search_url(self):
        return reverse("schools:search_url")
    class Meta:
        ordering = ['id']

class SchoolFilterOption(models.Model):
    filter_type = models.ForeignKey(SchoolFilter, null=True, on_delete = models.CASCADE, related_name='filter_options')
    schools = models.ManyToManyField(School, related_name='filter_options')
    title = models.CharField(max_length=250)
    class Meta:
        ordering = ['id']
class SchoolCategory(models.Model):
    schools = models.ManyToManyField(School, related_name='categories')
    title = models.CharField(max_length=250)
    main_filters = models.ForeignKey(SchoolFilter, null=True, on_delete = models.CASCADE, related_name='mcategories')
    second_filters = models.ManyToManyField(SchoolFilter, related_name='categories')
    number = models.IntegerField(default=1)
    class Meta:
        ordering = ['number']
    def get_absolute_url(self):
        return reverse("main:category", kwargs={"id": self.id})

class SubjectCategory(models.Model):
    schools = models.ManyToManyField(School, related_name='school_subject_categories')
    title = models.CharField(max_length=250)
    school_categories = models.ManyToManyField(SchoolCategory, related_name='subject_categories')
    def delete_url(self):
        return reverse("schools:subject_delete_url")
    def create_url(self):
        return reverse("schools:subject_create_url")
    def search_url(self):
        return reverse("schools:search_url")
    class Meta:
        ordering = ['title']

class SubjectAge(models.Model):
    schools = models.ManyToManyField(School, related_name='school_subject_ages')
    title = models.CharField(max_length=250)
    def delete_url(self):
        return reverse("schools:age_delete_url")
    def create_url(self):
        return reverse("schools:age_create_url")
    def search_url(self):
        return reverse("schools:search_url")
    class Meta:
        ordering = ['id']

class SubjectLevel(models.Model):
    schools = models.ManyToManyField(School, related_name='school_subject_levels')
    title = models.CharField(max_length=250)
    def delete_url(self):
        return reverse("schools:level_delete_url")
    def create_url(self):
        return reverse("schools:level_create_url")
    def search_url(self):
        return reverse("schools:search_url")
    class Meta:
        ordering = ['id']

class ElliteSchools(models.Model):
    schools = models.ManyToManyField(School, related_name='elite_list')

class FilterControl(models.Model):
    levels = models.ManyToManyField(SubjectLevel, related_name='filter_control')
    categories = models.ManyToManyField(SubjectCategory, related_name='filter_control')

class Office(models.Model):
    title = models.CharField(max_length=250)
    latitude = models.CharField(max_length=250, default='0.0')
    longtude = models.CharField(max_length=250, default='0.0')
    address = models.TextField(default='')
    region = models.CharField(max_length=250, default='')
    capacity = models.IntegerField(default=0)
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='school_offices')
    class Meta:
        ordering = ['id']
    def delete_url(self):
        return reverse("schools:office_delete_url")
    def create_url(self):
        return reverse("schools:office_create_url")
    def search_url(self):
        return reverse("schools:search_url")
    def create_cabinet_url(self):
        return reverse("schools:create_cabinet_url")

class Cabinet(models.Model):
    title = models.CharField(max_length=250)
    capacity = models.IntegerField(default=0)
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='cabinets')
    office = models.ForeignKey(Office, null=True, on_delete = models.CASCADE, related_name='cabinets')    
    class Meta:
        ordering = ['id']

class MoneyObject(models.Model):
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='money_object')
    title = models.CharField(max_length=250)
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']

class MoneyMonth(models.Model):
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='money_months')
    month = models.DateField(null = True, blank = True)
    money_spend = ArrayField(models.IntegerField(), default = list)
    money_earn = ArrayField(models.IntegerField(), default = list)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']
