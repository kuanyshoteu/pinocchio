from django.contrib import admin

# Register your models here.
from .models import *
from accounts.models import CRMColumn, CRMCard

class MoneyMonthModelAdmin(admin.ModelAdmin):
    list_display = ["school","month"]
    class Meta:
        model = MoneyMonth
admin.site.register(MoneyMonth, MoneyMonthModelAdmin)

class SchoolModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = School
admin.site.register(School, SchoolModelAdmin)

class CRMColumnModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["title"]
    class Meta:
        model = CRMColumn
admin.site.register(CRMColumn, CRMColumnModelAdmin)

class CRMCardModelAdmin(admin.ModelAdmin):
    list_display = ["name","id", "phone", "mail", "author_profile", "timestamp"]
    list_display_links = ["name"]
    list_filter = ["school","author_profile"]

    search_fields = ["name"]
    class Meta:
        model = CRMCard
admin.site.register(CRMCard, CRMCardModelAdmin)

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

class SubjectLevelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = SubjectLevel
admin.site.register(SubjectLevel, SubjectLevelAdmin)

class FilterControlAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    class Meta:
        model = FilterControl
admin.site.register(FilterControl, FilterControlAdmin)

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

class SchoolBannerAdmin(admin.ModelAdmin):
    list_display = ["id", "school"]
    list_display_links = ["id"]
    list_filter = ["id"]
    class Meta:
        model = SchoolBanner
admin.site.register(SchoolBanner, SchoolBannerAdmin)

class MoneyObjectAdmin(admin.ModelAdmin):
    list_display = ["id", "school", "amount", "timestamp"]
    list_display_links = ["id"]
    list_filter = ["school", "timestamp"]
    class Meta:
        model = MoneyObject
admin.site.register(MoneyObject, MoneyObjectAdmin)
