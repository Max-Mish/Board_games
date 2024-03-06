from django.contrib import admin

from .models import Description, Category, Game, BookedDate, GameItem


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ["description_text", "n_players", "duration", "difficulty"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "publisher", "cost"]


@admin.register(GameItem)
class GameItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_id', 'display_booked_dates']

    def display_booked_dates(self, obj):
        return ", ".join([str(date) for date in obj.booked_dates.all()])


@admin.register(BookedDate)
class BookedDateAdmin(admin.ModelAdmin):
    list_display = ['id', 'date']
