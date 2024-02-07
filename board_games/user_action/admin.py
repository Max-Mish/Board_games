from django.contrib import admin

from .models import Booking, Vote


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["game", "user", "return_date", "opening_date", "closing_date"]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "choice"]
