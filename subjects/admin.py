from django.contrib import admin

# Register your models here.
from .models import *

class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ["title","content","cost_period", "get_school", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = Subject
    def get_school(self, obj):
        return obj.school.title        

admin.site.register(Subject, SubjectModelAdmin)

class FilterDataModelAdmin(admin.ModelAdmin):
    list_display = ["get_author","crm_notices","payment_notices"]
    list_display_links = ["get_author"]
    list_filter = ["author"]
    class Meta:
        model = FilterData
    def get_author(self, obj):
        if obj.author:
            return obj.author.first_name        
        else:
            return 'no_author'

admin.site.register(FilterData, FilterDataModelAdmin)

class DayModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    class Meta:
        model = Day

admin.site.register(Day, DayModelAdmin)

class TimePeriodModelAdmin(admin.ModelAdmin):
    list_display = ["start", "end", 'num']
    list_display_links = ["start", "end"]
    list_filter = ["school","start", "end"]
    class Meta:
        model = TimePeriod

admin.site.register(TimePeriod, TimePeriodModelAdmin)

class LectureModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'cell']
    list_display_links = ["id"]
    list_filter = ["subject", "squad"]

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


class SubjectBillModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'start',"get_name", "get_squad", "get_subject"]
    list_display_links = ["id"]
    class Meta:
        model = SubjectBill
    def get_name(self, obj):
        if obj.bill_data:
            return obj.bill_data.card.name
        return '_'
    def get_subject(self, obj):
        if obj.subject:
            return obj.subject.title
        return '_'
    def get_squad(self, obj):
        if obj.bill_data:
            return obj.bill_data.squad.title
        return '_'
admin.site.register(SubjectBill, SubjectBillModelAdmin)
