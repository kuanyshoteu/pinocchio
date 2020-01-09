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
    list_display = ["id", 'get_teacher','get_squad', 'get_subject', 'get_student','present']
    list_display_links = ["id"]
    list_filter = ["teacher"]
    class Meta:
        model = Attendance
    def get_squad(self, obj):
        return obj.squad.title
    def get_subject(self, obj):
        return obj.subject.title
    def get_student(self, obj):
        return obj.student.first_name
    def get_teacher(self, obj):
        if obj.teacher:
            return obj.teacher.first_name
        return 'None'

admin.site.register(Attendance, AttendanceModelAdmin)

class NeedMoneyModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'get_squad', 'get_card', 'money']
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

class DiscountSchoolModelAdmin(admin.ModelAdmin):
    list_display = ['id',"title", 'school', 'amount', 'discount_type']
    list_display_links = ["title"]
    class Meta:
        model = DiscountSchool
admin.site.register(DiscountSchool, DiscountSchoolModelAdmin)

class PaymentHistoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', "get_school", 'timestamp', 'get_user', 'get_squad', 'get_action_author']
    list_display_links = ["id"]
    class Meta:
        model = PaymentHistory
    def get_school(self, obj):
        return obj.school.title
    def get_user(self, obj):
        return obj.user.first_name
    def get_squad(self, obj):
        return obj.squad.title
    def get_action_author(self, obj):
        return obj.action_author.first_name

admin.site.register(PaymentHistory, PaymentHistoryModelAdmin)
