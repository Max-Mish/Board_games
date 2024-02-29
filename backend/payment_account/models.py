from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.shortcuts import get_object_or_404
from djmoney.models import fields


class Account(models.Model):
    user_uuid = models.UUIDField(unique=True, editable=False, db_index=True)
    balance = fields.MoneyField(
        verbose_name=None,
        name=None,
        max_digits=11,
        default_currency='RUB',
        decimal_places=2,
        default=fields.Money('0.00', 'RUB'),
        validators=[MinValueValidator(0, message='Insufficient Funds')]
    )

    @classmethod
    def add_change_balance_method(cls, pk, amount, operation_type):
        if amount < 0:
            raise ValueError('Should be positive value')
        with transaction.atomic():
            account = get_object_or_404(
                cls.objects.select_for_update(),
                pk=pk,
            )
            if operation_type == 'DEPOSIT':
                account.balance += fields.Money(amount, 'RUB')
            elif operation_type == 'WITHDRAW':
                account.balance -= fields.Money(amount, 'RUB')
            account.save()
        return account

    def __str__(self) -> str:
        return f'User uuid: {self.user_uuid}'


class BalanceChange(models.Model):
    class TransactionType(models.TextChoices):
        WITHDRAW = ('WD', 'WITHDRAW')
        DEPOSIT = ('DT', 'DEPOSIT')

    account_id = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='balance_changes',
    )
    amount = models.DecimalField(
        max_digits=11,
        validators=[MinValueValidator(0, message='Should be positive value')],
        decimal_places=2,
        editable=False,
    )
    date_time_creation = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    is_accepted = models.BooleanField(default=False)
    operation_type = models.CharField(max_length=20, choices=TransactionType.choices)

    def __str__(self) -> str:
        return (
            f'Account id:  {self.account_id} '
            f'Date time of creation: {self.date_time_creation}'
            f'Amount: {self.amount}'
        )

    class Meta:
        ordering = ['-date_time_creation']


class PaymentCommission(models.Model):
    payment_service = models.CharField(max_length=30, unique=True)
    payment_type = models.CharField(max_length=50, verbose_name='type_of_payment')
    commission = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Type of payment: {self.payment_type}' f'Commission amount: {self.commission}'
