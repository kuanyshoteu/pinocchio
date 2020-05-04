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
    list_display = ["id", 'get_post']
    list_display_links = ["id"]
    class Meta:
        model = PostPart
    def get_post(self, obj):
        return obj.post.title + '; id=' + str(obj.post.id)

admin.site.register(PostPart, PostPartModelAdmin)