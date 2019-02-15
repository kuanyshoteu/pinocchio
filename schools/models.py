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

    address = models.CharField(max_length=250,default='')

    class Meta:
        ordering = ['title']
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("schools:detail")
    def get_delete_url(self):
        return reverse("schools:delete", kwargs={"id": self.id})
    def get_update_url(self):
        return reverse("schools:update", kwargs={"id": self.id})
    def get_list_url(self):
        return reverse("schools:list")
    def get_markdown(self):
        return mark_safe(markdown(self.content))
    def register_to_school(self):
        return reverse("schools:register_to_school")       

