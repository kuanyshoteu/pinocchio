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
from django.contrib.postgres.fields import ArrayField

from accounts.models import Profile
from papers.models import Lesson, Course
from schools.models import School

class Folder(models.Model):
    school = models.ForeignKey(School, default=1, on_delete = models.CASCADE, related_name='school_folders') 
    author_profile = models.ForeignKey(Profile, null = True, on_delete = models.CASCADE, related_name='folders')
    title = models.TextField()
    parent = models.ForeignKey("self",  null = True, on_delete = models.CASCADE, related_name = 'childs')
    children = models.ManyToManyField("self")
    lesson_list = models.ManyToManyField(Lesson, related_name='folder')
    
    class Meta:
        ordering = ['id']
    def get_absolute_url(self):
        return reverse("library:get_absolute_url", kwargs={"folder_id": self.id})
    def delete_folder_url(self):
        return reverse("library:delete_folder_url")
    def change_name_url(self):
        return reverse("library:change_name_url")


class Cache(models.Model):
    author_profile = models.ForeignKey(Profile, null = True, on_delete = models.CASCADE, related_name='cache')
    object_type = models.TextField(default='lesson')
    object_id = models.IntegerField(null = True)
    action = models.TextField(default='copy')
    previous_parent = models.IntegerField(null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    full = models.BooleanField(default = False)

