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
    list_filter = ["student"]
    class Meta:
        model = Attendance

admin.site.register(Attendance, AttendanceModelAdmin)

class NeedMoneyModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'get_squad', 'get_card', 'money', 'bill', 'lesson_bill']
    list_display_links = ["id"]
    list_filter = ["squad", 'card']
    class Meta:
        model = NeedMoney
    def get_squad(self, obj):
        return obj.squad.title
    def get_card(self, obj):
        return obj.card.name

admin.site.register(NeedMoney, NeedMoneyModelAdmin)

class BugModelAdmin(admin.ModelAdmin):
    list_display = ["text", 'timestamp']
    list_display_links = ["text"]
    class Meta:
        model = Bug
admin.site.register(Bug, BugModelAdmin)


