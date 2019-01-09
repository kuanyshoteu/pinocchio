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

def upload_location(instance, filename):
    CourseModel = instance.__class__
    if CourseModel.objects.order_by("id").last():
        new_id = CourseModel.objects.order_by("id").last().id + 1
    else:
        new_id=0
    return "%s/%s" %(instance.id, filename)


class Squad(models.Model):
    curator = models.ManyToManyField(Profile, default=1, related_name='curators_squads')
    students = models.ManyToManyField(Profile, default=1, related_name='squads')

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
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
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    
    content = models.TextField(default='')
    slogan = models.CharField(max_length=250, default='')

    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    cabinet = models.CharField(max_length=250,default='')

    class Meta:
        ordering = ['title']
    def __unicode__(self):
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

class SquadWeek(models.Model):
    squad = models.ForeignKey(Squad, default=1, on_delete = models.CASCADE, related_name='weeks')
    actual = models.BooleanField(default = False)
    class Meta:
        ordering = ['id']

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

class Follow(models.Model):
    author_profile = models.ForeignKey(Profile, default=1, on_delete = models.PROTECT)
    group = models.ForeignKey(Squad, default=1, on_delete = models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']
    
    def get_api_deletefollow_url(self):
        return reverse("accounts:deletefollow-api-toggle", kwargs={"id": self.id})

class SquadCategory(models.Model):
    title = models.TextField(default = '')
    squads = models.ManyToManyField(Squad, default=1, related_name='squad_categories')
