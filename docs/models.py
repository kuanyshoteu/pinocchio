from __future__ import unicode_literals
from django.utils.text import slugify
from accounts.models import Profile

from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField

from django.urls import reverse

from django.db import models
from accounts.models import Profile

def upload_location(instance, filename):
    CardModel = instance.__class__
    if CardModel.objects.order_by("id").last():
        new_id = CardModel.objects.order_by("id").last().id + 1
    return "%s" %(filename)

class Document(models.Model):
    file = models.FileField(upload_to=upload_location, null = True)

class Metka(models.Model):
    name = models.CharField(max_length=255)

class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return super(CommentManager, self).filter(content_type=content_type, object_id= instance.id)

    def filter_by_author(self, author):
        return super(CommentManager, self).filter(user= author)


class Comment(models.Model):
    author_profile = models.ForeignKey(Profile, default=1, on_delete = models.PROTECT, related_name='comments')
    content = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    card = models.ForeignKey("Card", related_name='comments', default=1, on_delete = models.CASCADE)
    ffile = models.ManyToManyField(Document, related_name='ffile')
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field",)
    height_field = models.IntegerField(default=0, null = True)
    width_field = models.IntegerField(default=0, null = True)
    
    objects = CommentManager()

    class Meta:
        ordering = ['timestamp']

    def __unicode__(self):
        return str(self.user.username)


class Board(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Column(models.Model):
    board = models.ForeignKey('Board', related_name='columns', on_delete = models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{} - {}'.format(self.board.name, self.title)

class Card(models.Model):
    column = models.ForeignKey('Column', related_name='cards', on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    description = models.TextField(blank = True,null = True,default='')
    user_list = models.ManyToManyField(Profile, related_name='cards')
    metka_list = models.ManyToManyField(Metka, related_name='cards')
    doc_list = models.ManyToManyField(Document, related_name='cards')
    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{} - {} - {}'.format(self.column.board.name, self.column.title, self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("docs:card", kwargs={"card_id": self.id, "card_slug":self.slug})

    def change_text_url(self):
        return reverse("docs:change_card_text_url")
    def add_user_url(self):
        return reverse("docs:add_user_url")
    def add_metka_url(self):
        return reverse("docs:add_metka_url")

