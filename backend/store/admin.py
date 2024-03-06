from django.contrib import admin

from store.models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["address", "open_hours", "email", "phone_number", "manager"]
