from django.contrib import admin

from .models import *


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["user", "id" ]
    list_display_links = ["user"]

    search_fields = ["user"]
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileModelAdmin)

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

