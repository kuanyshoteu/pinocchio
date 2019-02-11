from django.contrib import admin

from .models import *


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["first_name", "id" ]
    list_display_links = ["first_name"]

    search_fields = ["first_name"]
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileModelAdmin)

class ProfileSchedule(admin.ModelAdmin):
    list_display = ["x", "y"]
    list_display_links = ["x", "y"]
    class Meta:
        model = ProfileScheduleCell

admin.site.register(ProfileScheduleCell, ProfileSchedule)

class ZaiavkaModelAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "phone"]
    list_display_links = ["name"]
    list_filter = ["name"]

    search_fields = ["name", "phone"]
    class Meta:
        model = Zaiavka

admin.site.register(Zaiavka, ZaiavkaModelAdmin)

class MainPageModelAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    
    class Meta:
        model = MainPage


admin.site.register(MainPage, MainPageModelAdmin)

