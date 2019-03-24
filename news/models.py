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
from schools.models import School

def upload_location(instance, filename):
    CourseModel = instance.__class__
    if CourseModel.objects.order_by("id").last():
        new_id = CourseModel.objects.order_by("id").last().id + 1
    else:
        new_id=0
    return "%s/%s" %(instance.id, filename)


class Post(models.Model):
    school = models.ForeignKey(School, default=1, on_delete = models.CASCADE, related_name='school_posts') 
    author_profile = models.ForeignKey(Profile, default=1, on_delete = models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)

    content = models.TextField(default='')
    image = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)

    class Meta:
        ordering = ['-id']
    def __unicode__(self):
        return self.id
    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"id": self.id})
    def get_delete_url(self):
        return reverse("news:delete")
    def get_update_url(self):
        return reverse("news:update", kwargs={"id": self.id})
    def get_list_url(self):
        return reverse("news:list")
    def get_markdown(self):
        return mark_safe(markdown(self.content))

