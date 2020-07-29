from django.contrib import admin

# Register your models here.
from .models import *

class LessonFolderModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = LessonFolder
admin.site.register(LessonFolder, LessonFolderModelAdmin)

class PaperModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = Paper
admin.site.register(Paper, PaperModelAdmin)

class LessonModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = Lesson
admin.site.register(Lesson, LessonModelAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "lesson","level","author_profile","timestamp"]
    list_display_links = ["id"]
    list_filter = ["level"]
    class Meta:
        model = Comment
admin.site.register(Comment, CommentAdmin)

class SubthemeModelAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    list_filter = ["id"]
    class Meta:
        model = Subtheme
admin.site.register(Subtheme, SubthemeModelAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = Course
admin.site.register(Course, CourseAdmin)
