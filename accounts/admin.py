from django.contrib import admin

from .models import *


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["first_name", "id" ]
    list_display_links = ["first_name"]

    search_fields = ["first_name"]
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileModelAdmin)

class ProfessionAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    class Meta:
        model = Profession
admin.site.register(Profession, ProfessionAdmin)

class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "salary", "profession"]
    list_display_links = ["title"]
    class Meta:
        model = JobCategory
admin.site.register(JobCategory, JobCategoryAdmin)

class ZaiavkaModelAdmin(admin.ModelAdmin):
    list_display = ["first_name", "id", "phone"]
    list_display_links = ["first_name"]
    list_filter = ["first_name"]
    search_fields = ["first_name", "phone"]
    class Meta:
        model = Zaiavka

admin.site.register(Zaiavka, ZaiavkaModelAdmin)

class CorruptionAdmin(admin.ModelAdmin):
    list_display = ["text", "id",]
    list_display_links = ["id"]
    list_filter = ["text"]
    search_fields = ["text"]
    class Meta:
        model = Corruption

admin.site.register(Corruption, CorruptionAdmin)

class MissLessonAdmin(admin.ModelAdmin):
    list_display = ["profile", "text",]
    list_display_links = ["profile"]
    list_filter = ["text"]
    search_fields = ["text"]
    class Meta:
        model = MissLesson
admin.site.register(MissLesson, MissLessonAdmin)
