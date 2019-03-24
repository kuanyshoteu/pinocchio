from django.contrib import admin

# Register your models here.
from .models import *

class SchoolModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = School
admin.site.register(School, SchoolModelAdmin)

class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = SubjectCategory
admin.site.register(SubjectCategory, SubjectCategoryAdmin)

class SubjectAgeAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = SubjectAge
admin.site.register(SubjectAge, SubjectAgeAdmin)

class CabinetAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = Cabinet
admin.site.register(Cabinet, CabinetAdmin)

class OfficeAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = Office
admin.site.register(Office, OfficeAdmin)
