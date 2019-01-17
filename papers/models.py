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
from squads.models import Squad
from tasks.models import Task

def upload_location(instance, filename):
    PaperModel = instance.__class__
    new_id = PaperModel.objects.order_by("id").last().id + 1
    return "%s" %(filename)

class Subtheme(models.Model):
    title = models.CharField(max_length=250)
    task_list = models.ManyToManyField(Task, related_name='subthemes')
    content = models.TextField(default='')
    video = models.FileField(default='')
    file = models.FileField(default='')
    youtube_video_link = models.TextField(default='')
    def new_task_url(self):
        return reverse("papers:new_task_url")
    def add_task_url(self):
        return reverse("papers:add_task_url")        
    def rename_subtheme_url(self):
        return reverse("papers:rename_subtheme_url")
    def rewrite_subtheme_url(self):
        return reverse("papers:rewrite_subtheme_url")
    def get_markdown(self):
        return mark_safe(markdown(self.content))
    def delete_subtheme_url(self):
        return reverse("papers:delete_subtheme_url")
        
class Paper(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='paper_author')
    subthemes = models.ManyToManyField(Subtheme, related_name='papers')
    done_by = models.ManyToManyField(Profile, related_name='done_papers')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        return reverse("papers:detail", kwargs={"slug": self.slug})

    def api_url_add_group(self):
        return reverse("papers:add-group-toggle")
    def delete_paper_url(self):
        return reverse("papers:delete_paper_url")
    def add_subtheme_url(self):
        return reverse("papers:add_subtheme_url")
    def rename_paper_url(self):
        return reverse("papers:rename_paper_url")

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    class Meta:
        ordering = ['id']

def create_slug(instance, new_slug=None):
    if len(Paper.objects.all()) > 0:
        paper = Paper.objects.all()[len(Paper.objects.all())-1]
        slug = slugify('qqq' + str(paper.id + 1))
        if len(Paper.objects.filter(slug=slug)) > 0:
            slug = slugify('qqq' + str(paper.id + 1) + 'q')
    else:
        slug = slugify('0')
    return slug 

def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_course_receiver, sender=Paper)
    
class Lesson(models.Model):
    title = models.CharField(max_length=250)
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='lesson_author')
    is_homework = models.BooleanField(default=False)
    papers = models.ManyToManyField(Paper, related_name='lessons')
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='liked_lessons')
    dislikes = models.ManyToManyField(Profile, related_name='disliked_lessons')
    done_by = models.ManyToManyField(Profile, related_name='done_lessons')
    
    def add_paper_url(self):
        return reverse("papers:add_paper_url")
    def change_name_url(self):
        return reverse("papers:change_name_url")
    def get_absolute_url(self):
        return reverse("papers:lesson_absolute_url", kwargs={"lesson_id": self.id})
    def delete_lesson_url(self):
        return reverse("papers:delete_lesson_url")
    def check_paper_url(self):
        return reverse("papers:check_paper_url")
    def new_comment_url(self):
        return reverse("papers:new_comment_url")
    def like_url(self):
        return reverse("papers:lesson_like_url")
    def dislike_url(self):
        return reverse("papers:lesson_dislike_url")
    class Meta:
        ordering = ['id']

class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, on_delete = models.CASCADE, related_name='comments')
    level = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='hiscomments')
    content = models.TextField(default='')
    parent = models.ForeignKey('self', null=True, on_delete = models.CASCADE, related_name='children')
    likes = models.ManyToManyField(Profile, related_name='liked_comments')
    dislikes = models.ManyToManyField(Profile, related_name='disliked_comments')
    class Meta:
        ordering = ['timestamp']
    def like_url(self):
        return reverse("papers:like_url")
    def dislike_url(self):
        return reverse("papers:dislike_url")

class Course(models.Model):
    title = models.CharField(max_length=250)
    lessons = models.ManyToManyField(Lesson, related_name='courses')
    author_profile = models.ForeignKey(Profile, null=True, on_delete = models.CASCADE, related_name='hiscourses')
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field",)
    height_field = models.IntegerField(default=0, null = True)
    width_field = models.IntegerField(default=0, null = True)

    cost = models.IntegerField(default = 0)
    content = models.TextField(default='')
    students = models.ManyToManyField(Profile, default=1, related_name='courses')
    done_by = models.ManyToManyField(Profile, related_name='done_courses')

    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)
    stars = ArrayField(models.IntegerField(), default = [])
    class Meta:
        ordering = ['timestamp']
    def get_absolute_url(self):
        return reverse("papers:course_absolute_url", kwargs={"course_id": self.id})
    def get_seller_url(self):
        return reverse("papers:course_seller_url", kwargs={"course_id": self.id})
    def get_update_url(self):
        return reverse("papers:course_update_url", kwargs={"course_id": self.id})
    def delete_course_url(self):
        return reverse("papers:delete_course_url")
    def get_markdown(self):
        return mark_safe(markdown(self.content))
    def add_lesson_url(self):
        return reverse("papers:add_lesson_url")
    def like_url(self):
        return reverse("papers:course_like_url")
    def dislike_url(self):
        return reverse("papers:course_dislike_url")
