from django.contrib import admin

from .models import *


class CardModelAdmin(admin.ModelAdmin):
    list_display = ["title", "id", "column" ]
    list_display_links = ["title"]

    class Meta:
        model = Card

admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Card, CardModelAdmin)
admin.site.register(Comment)

admin.site.register(Metka)
admin.site.register(Document)
