from django.contrib import admin

# Register your models here.
from .models import *

class TaskModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'text']
    list_display_links = ["id"]
    list_filter = ["text"]

    search_fields = ["text"]
    class Meta:
        model = Task

admin.site.register(Task, TaskModelAdmin)

class TagModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'title']
    list_display_links = ["id"]
    class Meta:
        model = ProblemTag

admin.site.register(ProblemTag, TagModelAdmin)