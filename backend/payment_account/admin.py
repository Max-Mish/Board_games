from django.contrib import admin


from .models import Account, PaymentCommission


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user_uuid', 'balance_currency', 'balance']


# @admin.register(PaymentCommission)
# class PaymentCommissionAdmin(admin.ModelAdmin):
#     list_display = "__all__"


@admin.register(PaymentCommission)
class PaymentServiceAdmin(admin.ModelAdmin):
    list_display = ["payment_service"]
