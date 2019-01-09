from django.contrib import admin

# Register your models here.
from .models import *
from subjects.models import SquadCell, Attendance

class SquadModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = Squad

admin.site.register(Squad, SquadModelAdmin)


class FollowModelAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    class Meta:
        model = Follow

admin.site.register(Follow, FollowModelAdmin)

class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'student', 'squad_cell']
    list_display_links = ["id"]
    class Meta:
        model = Attendance

admin.site.register(Attendance, AttendanceModelAdmin)

class SquadCellAdmin(admin.ModelAdmin):
    list_display = ["id", 'squad', 'date']
    list_display_links = ["id"]
    class Meta:
        model = SquadCell

admin.site.register(SquadCell, SquadCellAdmin)

class SquadWeekAdmin(admin.ModelAdmin):
    list_display = ["id", 'squad']
    list_display_links = ["id"]
    class Meta:
        model = SquadWeek

admin.site.register(SquadWeek, SquadWeekAdmin)

