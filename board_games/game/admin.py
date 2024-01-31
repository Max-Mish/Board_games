from django.contrib import admin

from .models import Description, Category, BoardGame


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ["description_text", "n_players", "duration", "difficulty"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "publisher", "cost"]

