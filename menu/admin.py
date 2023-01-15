from django.contrib import admin

from menu.models import Menu, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', "parent")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", )
