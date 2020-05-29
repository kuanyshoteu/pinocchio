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
from todolist.models import Document
from schools.models import School

class DocumentFolder(models.Model):
    school = models.ForeignKey(School, null = True, on_delete = models.CASCADE, related_name='school_docfolders') 
    author_profile = models.ForeignKey(Profile, null = True, on_delete = models.CASCADE, related_name='docfolders')
    title = models.TextField()
    parent = models.ForeignKey("self", null = True, on_delete = models.CASCADE, related_name = 'docchilds')
    children = models.ManyToManyField("self")
    files = models.ManyToManyField(Document, related_name='docfolder')
    
    class Meta:
        ordering = ['id']
    def get_absolute_url(self):
        return reverse("documents:get_absolute_url", kwargs={"folder_id": self.id})
    def delete_folder_url(self):
        return reverse("documents:delete_folder_url")
    def change_docname_url(self):
        return reverse("documents:change_docname_url")

class DocumentCache(models.Model):
    author_profile = models.ForeignKey(Profile, null = True, on_delete = models.CASCADE, related_name='doccache')
    object_type = models.TextField(default='')
    object_id = models.IntegerField(null = True)
    action = models.TextField(default='')
    previous_parent = models.IntegerField(null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    full = models.BooleanField(default = False)

