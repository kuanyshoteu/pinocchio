from django.contrib import admin

# Register your models here.
from .models import *

class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ["title", "school", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    class Meta:
        model = Subject

admin.site.register(Subject, SubjectModelAdmin)

class DayModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    class Meta:
        model = Day

admin.site.register(Day, DayModelAdmin)

class TimePeriodModelAdmin(admin.ModelAdmin):
    list_display = ["start", "end"]
    list_display_links = ["start", "end"]
    list_filter = ["start", "end"]

    class Meta:
        model = TimePeriod

admin.site.register(TimePeriod, TimePeriodModelAdmin)

class LectureModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'cell']
    list_display_links = ["id"]
    list_filter = ["subject", "squad", "school"]

    class Meta:
        model = Lecture

admin.site.register(Lecture, LectureModelAdmin)

class SubjectMaterialsAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "number"]
    list_display_links = ["id"]
    list_filter = ["subject"]

    class Meta:
        model = SubjectMaterials

admin.site.register(SubjectMaterials, SubjectMaterialsAdmin)

class CellModelAdmin(admin.ModelAdmin):
    list_display = ['id', "day", "time_period"]
    list_display_links = ["day"]
    list_filter = ["day"]

    class Meta:
        model = Cell

admin.site.register(Cell, CellModelAdmin)

class CacheAttendanceModelAdmin(admin.ModelAdmin):
    list_display = ["id", "profile", "subject"]
    list_display_links = ["id"]

    class Meta:
        model = CacheAttendance

admin.site.register(CacheAttendance, CacheAttendanceModelAdmin)
