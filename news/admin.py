from django.contrib import admin

# Register your models here.
from .models import *

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","title"]
    list_display_links = ["id"]
    search_fields = ["title"]
    class Meta:
        model = Post
admin.site.register(Post, PostModelAdmin)

class PostPartModelAdmin(admin.ModelAdmin):
    list_display = ["id","content"]
    list_display_links = ["id"]
    search_fields = ["content"]
    class Meta:
        model = PostPart
admin.site.register(PostPart, PostPartModelAdmin)