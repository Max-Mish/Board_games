import uuid
from datetime import timedelta, datetime
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from djmoney.models import fields

from payment_account.models import Account
from user_action.models import Booking


class ItemPurchase(models.Model):
    MAX_ITEM_PRICE = 10000

    account_from = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='item_purchase_account_from',
    )
    account_to = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='item_purchase_account_to',
    )
    booking_id = models.ForeignKey(
        Booking,
        on_delete=models.PROTECT,
        related_name='booking_info',
        null=True,
    )
    item_price = fields.MoneyField(verbose_name=None,
                                   name=None,
                                   max_digits=11,
                                   default_currency='RUB',
                                   decimal_places=2,
                                   default=fields.Money('0.00', 'RUB'),
                                   validators=(
                                       MinValueValidator(0, message='Should be positive value'),
                                       MaxValueValidator(
                                           MAX_ITEM_PRICE,
                                           message=f'Should be not greater than {MAX_ITEM_PRICE}',
                                       ),
                                   ),
                                   )

    def __str__(self) -> str:
        return (
            f'Account from: {self.account_from} -> '
            f'Account to: {self.account_to} '
            f'Item_uid: {self.booking_id}'
        )


class Invoice(models.Model):
    invoice_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    item_purchases = models.ManyToManyField(ItemPurchase)
    price_with_commission = fields.MoneyField(verbose_name=None,
                                              name=None,
                                              max_digits=11,
                                              default_currency='RUB',
                                              decimal_places=2,
                                              default=fields.Money('0.00', 'RUB'),
                                              validators=[MinValueValidator(0, message='Should be positive value')],
                                              )
    is_paid = models.BooleanField(default=False)
    created_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    @property
    def items_sum_price(self):
        return Decimal(
            sum(
                self.item_purchases.all().values_list('item_price', flat=True),
            ),
        )

    @classmethod
    def get_positive_attempts_for_period(cls, user_account: Account) -> int:
        return cls._get_invoice_attempts_for_period(
            is_paid=True,
            user_account=user_account,
        )

    @classmethod
    def get_negative_attempts_for_period(cls, user_account: Account) -> int:
        return cls._get_invoice_attempts_for_period(
            is_paid=False,
            user_account=user_account,
        )

    @classmethod
    def _get_invoice_attempts_for_period(cls, is_paid: bool, user_account: Account) -> int:
        start_date = datetime.now() - timedelta(minutes=60)
        return cls.objects.filter(
            Q(item_purchases__account_from=user_account)
            & Q(is_paid=is_paid)
            & Q(created_date__gte=start_date),
        ).count()

    def __str__(self):
        return f'{self.invoice_id}'

    class Meta:
        ordering = ['-created_date']
