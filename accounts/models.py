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
from schools.models import School

def upload_location(instance, filename):
    ProfileModel = instance.__class__
    if ProfileModel.objects.order_by("id").last():
        new_id = ProfileModel.objects.order_by("id").last().id + 1
    return "%s" %(filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    coins = models.IntegerField(default=0)
    first_name = models.TextField(blank = True,null = True,default='')
    is_trener = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    is_ceo = models.BooleanField(default=False)

    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='students')
    
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
    
    class Meta:
        ordering = ['-coins']

    def get_absolute_url(self):
        self.user.username = self.user.username.replace(' ', '_')
        self.user.username = self.user.username.replace('Қ', 'К')
        self.user.username = self.user.username.replace('қ', 'к')
        return reverse("accounts:profile", kwargs={"user": self.user})

    def get_api_change_url(self):
        return reverse("accounts:change-api-toggle")
    def city_api_url(self):
        return reverse("main:city_api_url")
    def filial_api_url(self):
        return reverse("main:filial_api_url")
    def subject_api_url(self):
        return reverse("main:subject_api_url")

    def change_page_url(self):
        return reverse("accounts:change_page_url")
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
    def change_status_url(self):
        return reverse("accounts:change_status_url")
    def change_url(self):
        return reverse("accounts:change_url")
    def tell_about_corruption(self):
        return reverse("accounts:tell_about_corruption")
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Zaiavka(models.Model):
    name = models.TextField()
    phone = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']
    
    def get_api_deletezaiavka_url(self):
        return reverse("accounts:deletezaiavka-api-toggle", kwargs={"id": self.id})
    
class MainPage(models.Model):
    admin_name = models.TextField(default = 'admin2')
    title = models.TextField(default = 'Летняя программа')
    text = models.TextField(default = 'text')
    schedule_time_periods = ArrayField(models.TextField(), default = [''])

    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field",)
    height_field = models.IntegerField(default=0, null = True)
    width_field = models.IntegerField(default=0, null = True)
 
    folder_image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field2", 
            height_field="height_field2",)
    height_field2 = models.IntegerField(default=0, null = True)
    width_field2 = models.IntegerField(default=0, null = True)

    paper_image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field3", 
            height_field="height_field3",)
    height_field3 = models.IntegerField(default=0, null = True)
    width_field3 = models.IntegerField(default=0, null = True)

    squad_image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field4", 
            height_field="height_field4",)
    height_field4 = models.IntegerField(default=0, null = True)
    width_field4 = models.IntegerField(default=0, null = True)

    def city_api_url(self):
        return reverse("main:city_api_url")
    def filial_api_url(self):
        return reverse("main:filial_api_url")
    def subject_api_url(self):
        return reverse("main:subject_api_url")
    def main_url(self):
        return reverse("main:home")
    def save_zaiavka_url(self):
        return reverse("main:save_zaiavka_url")
    def get_markdown(self):
        return mark_safe(markdown(self.text))
        

def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

class Corruption(models.Model):
    text = models.TextField(default='')
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='his_messages')
    school = models.ForeignKey(School, null=True, on_delete = models.CASCADE, related_name='corruptions')
