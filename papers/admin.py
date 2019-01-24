from django.contrib import admin

# Register your models here.
from .models import *

class PaperModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = Paper

class LessonModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    class Meta:
        model = Lesson

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "lesson","level","author_profile","timestamp"]
    list_display_links = ["id"]
    list_filter = ["level"]

    class Meta:
        model = Comment

class SubthemeModelAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    list_filter = ["id"]

    class Meta:
        model = Subtheme

class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    class Meta:
        model = Course

admin.site.register(Paper, PaperModelAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Lesson, LessonModelAdmin)
admin.site.register(Subtheme, SubthemeModelAdmin)
admin.site.register(Course, CourseAdmin)
