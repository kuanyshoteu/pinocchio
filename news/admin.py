from django.contrib import admin

# Register your models here.
from .models import *

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
