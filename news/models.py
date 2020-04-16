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
    title = models.TextField(default='')
    school = models.ForeignKey(School, default=1, on_delete = models.CASCADE, related_name='school_posts') 
    author_profile = models.ForeignKey(Profile, default=1, on_delete = models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='liked_posts')
    dislikes = models.ManyToManyField(Profile, related_name='disliked_posts')
    done_by = models.ManyToManyField(Profile, related_name='read_posts')
    slug = models.SlugField(unique=True, default="")
    order = models.IntegerField(default=0)
    priority = models.IntegerField(default=1)
    class Meta:
        ordering = ['order','timestamp']
    def __unicode__(self):
        return self.id
    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"slug": self.slug})
    def get_edit_url(self):
        return reverse("news:post_edit", kwargs={"slug": self.slug})

class PostPart(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete = models.CASCADE, related_name='parts')
    content = models.TextField(default='')
    video = models.FileField(null=True, blank=True)
    file = models.FileField(null=True,blank=True)
    youtube_video_link = models.TextField(default='')
    image = models.ImageField(upload_to=upload_location, 
            null=True,
            blank=True, 
            )
    order = models.IntegerField(default=0)
    show = models.BooleanField(default=True)
    class Meta: 
        ordering = ['order']
    def get_markdown(self):
        return mark_safe(markdown(self.content))
            
class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete = models.CASCADE, related_name='comments')
    level = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='postcomments')
    content = models.TextField(default='')
    parent = models.ForeignKey('self', null=True, on_delete = models.CASCADE, related_name='children')
    likes = models.ManyToManyField(Profile, related_name='liked_post_comments')
    dislikes = models.ManyToManyField(Profile, related_name='disliked_post_comments')
    class Meta:
        ordering = ['timestamp']
