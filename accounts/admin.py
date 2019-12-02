from django.contrib import admin

from .models import *


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["first_name", "id", "phone"]
    list_display_links = ["first_name"]
    list_filter = ["schools"]
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

class MissLessonAdmin(admin.ModelAdmin):
    list_display = ["profile", "text",]
    list_display_links = ["profile"]
    list_filter = ["text"]
    search_fields = ["text"]
    class Meta:
        model = MissLesson
admin.site.register(MissLesson, MissLessonAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["author_profile", "id", "itstype","text"]
    list_display_links = ["author_profile"]
    list_filter = ["itstype", 'school']
    class Meta:
        model = Notification
admin.site.register(Notification, NotificationAdmin)

class SkillAdmin(admin.ModelAdmin):
    list_display = ["id", "need_actions"]
    list_display_links = ["id"]
    class Meta:
        model = Skill
admin.site.register(Skill, SkillAdmin)

class HashtagAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    list_display_links = ["id"]
    list_filter = ['schools']
    class Meta:
        model = Hashtag
admin.site.register(Hashtag, HashtagAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "school", "author_profile", "text", "rating"]
    list_display_links = ["id"]
    list_filter = ['school', 'author_profile']
    class Meta:
        model = Review
admin.site.register(Review, ReviewAdmin)
