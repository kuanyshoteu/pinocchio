from django.contrib import admin

# Register your models here.
from .models import *
from subjects.models import Attendance

class SquadModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = Squad

admin.site.register(Squad, SquadModelAdmin)

class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'student']
    list_display_links = ["id", 'student']
    class Meta:
        model = Attendance

admin.site.register(Attendance, AttendanceModelAdmin)

