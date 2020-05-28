from django.contrib import admin

# Register your models here.
from .models import *
from accounts.models import CRMColumn, CRMCard

class HelpVideosModelAdmin(admin.ModelAdmin):
    list_display = ["title"]
    class Meta:
        model = HelpVideos
admin.site.register(HelpVideos, HelpVideosModelAdmin)
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

class SchoolFilterModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = SchoolFilter
admin.site.register(SchoolFilter, SchoolFilterModelAdmin)

class SchoolFilterOptionModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]

    search_fields = ["content"]
    class Meta:
        model = SchoolFilterOption
admin.site.register(SchoolFilterOption, SchoolFilterOptionModelAdmin)

class SchoolCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["title", "number", "id"]
    list_display_links = ["title"]
    list_filter = ["title"]
    class Meta:
        model = SchoolCategory
admin.site.register(SchoolCategory, SchoolCategoryModelAdmin)

class ElliteSchoolModelAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    class Meta:
        model = ElliteSchools
admin.site.register(ElliteSchools, ElliteSchoolModelAdmin)

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

class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ["id", "socialmedia", "username", "school"]
    list_display_links = ["id"]
    list_filter = ["school", "socialmedia"]
    class Meta:
        model = SocialMediaAccount
admin.site.register(SocialMediaAccount, SocialMediaAccountAdmin)

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    list_display_links = ["id"]
    class Meta:
        model = SocialMedia
admin.site.register(SocialMedia, SocialMediaAdmin)

class CityModelAdmin(admin.ModelAdmin):
    list_display = ["title"]
    class Meta:
        model = City
admin.site.register(City, CityModelAdmin)
