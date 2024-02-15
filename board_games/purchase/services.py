from decimal import Decimal

import rollbar
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from djmoney.money import Money
from yookassa import Payment

from payment_account.models import Account, BalanceChange
from payment_account.services import PaymentCalculation
from purchase.models import Invoice, ItemPurchase
from user_action.models import Booking


class InvoiceCreator:
    def __init__(self, income_data, payer_account):
        self.income_data = income_data
        self.payer_account = payer_account
        self.invoice_instance = None

        self.invoice_id = self.create_invoice_instance()

    def create_invoice_instance(self):
        list_of_item_purchase = []
        for item_payment_data in self.income_data['items_payment_data']:
            item_purchase = self.create_item_purchase_instance(
                self.payer_account,
                self.income_data['user_uuid_to'],
                item_payment_data,
            )
            list_of_item_purchase.append(item_purchase)
        money_data = (self.income_data['price_with_commission'], 'RUB')
        invoice = Invoice.objects.create(
            price_with_commission=money_data,
        )
        invoice.item_purchases.add(*list_of_item_purchase)
        self.invoice_instance = invoice
        return invoice.pk

    @staticmethod
    def create_item_purchase_instance(payer_account, receiver_account, item_payment_data):
        booking = Booking.objects.get(id=item_payment_data['booking_id'])
        account_to = get_object_or_404(Account, user_uuid=receiver_account)
        money_data = Money(item_payment_data['price'], 'RUB')

        item_purchase = ItemPurchase.objects.create(
            account_from=payer_account,
            account_to=account_to,
            item_price=money_data,
            booking_id=booking,
        )
        return item_purchase


def execute_invoice_operations(invoice_instance, payer_account, decrease_amount):
    with transaction.atomic():
        balance_change_object = BalanceChange.objects.create(
            account_id=payer_account,
            amount=decrease_amount,
            is_accepted=True,
            operation_type=BalanceChange.TransactionType.WITHDRAW,
        )

        Account.add_change_balance_method(
            pk=payer_account.pk,
            amount=Decimal(decrease_amount),
            operation_type='WITHDRAW'
        )

        invoice_instance.is_paid = True
        invoice_instance.save()


class ItemPurchaseRequest:
    def __init__(self, purchase_items_data):
        self.purchase_items_data = purchase_items_data
        self.user_account, _ = Account.objects.get_or_create(
            user_uuid=purchase_items_data['user_uuid_from'],
        )
        self._validate_income_data()

    def request_items_purchase(self):
        invoice_creator = InvoiceCreator(self.purchase_items_data, self.user_account)
        invoice_instance = invoice_creator.invoice_instance

        if self.purchase_items_data['payment_service'] == 'from_balance':
            execute_invoice_operations(
                invoice_instance=invoice_instance,
                payer_account=self.user_account,
                decrease_amount=invoice_instance.items_sum_price,
            )
            return 'Success'

        if self.purchase_items_data['payment_service'] == 'yookassa':
            balance_change = BalanceChange.objects.create(
                account_id=self.user_account,
                is_accepted=False,
                operation_type=BalanceChange.TransactionType.WITHDRAW,
                amount=self.purchase_items_data['price_with_commission']
            )
            price_without_commision = PaymentCalculation(self.purchase_items_data['payment_type'],
                                                         self.purchase_items_data['payment_service'],
                                                         self.purchase_items_data[
                                                             'price_with_commission']).calculate_payment_without_commission()
            payment = Payment.create({
                'amount': {
                    'value': self.purchase_items_data['price_with_commission'],
                    'currency': self.purchase_items_data['currency'],
                },
                'payment_method_data': {
                    'type': self.purchase_items_data['payment_type'],
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': self.purchase_items_data['return_url'],
                },
                'metadata': {
                    'table_id': balance_change.pk,
                    'user_id': self.user_account.pk,
                    'invoice_id': str(invoice_instance.pk)
                },
                'capture': True,
                'refundable': False,
                'description': 'Пополнение на ' + str(price_without_commision),
            })

            return payment.confirmation.confirmation_url

    def _validate_income_data(self):
        self._is_booking_right()
        if (
                self.purchase_items_data['payment_service'] == 'from_balance'
                and not self._is_enough_funds()
        ):
            raise ValidationError('Not enough funds on balance')
        if not self._is_invoice_price_correct()[0]:
            raise ValidationError(
                f'Invoice price and items sum price is not valid, requested price = {self._is_invoice_price_correct()[1]}')
        if self._is_invoice_attempts_exceeded():
            rollbar.report_message(
                f'Suspicious user behaviour {self.user_account.user_uuid}.',
                'info',
            )
            raise ValidationError(
                f'Too many purchase attempts for '
                f'last {60} minutes.',
            )

    def _is_enough_funds(self):
        return (
                self.user_account.balance.amount
                >= self.purchase_items_data['price_with_commission']
        )

    def _is_invoice_price_correct(self):
        items_sum_price = sum([item.get('price') for item in self.purchase_items_data.get('items_payment_data')])
        if self.purchase_items_data['payment_service'] == 'from_balance':
            compare_price = items_sum_price
        else:
            compare_price = PaymentCalculation(
                payment_type=self.purchase_items_data['payment_type'],
                payment_service=self.purchase_items_data['payment_service'],
                payment_amount=items_sum_price,
            ).calculate_payment_with_commission()
        return compare_price == self.purchase_items_data['price_with_commission'], compare_price

    def _is_booking_right(self):
        bookings_list = [
            item['booking_id'] for item in self.purchase_items_data['items_payment_data']
        ]

        if len(bookings_list) != len(Booking.objects.filter(id__in=bookings_list)):
            raise ValidationError('One of Bookings does not exist')

        if len(bookings_list) != len(Booking.objects.filter(id__in=bookings_list,
                                                            user_id=self.purchase_items_data['user_uuid_from'])):
            raise ValidationError('One of Bookings is not on paying user')

        for item in ItemPurchase.objects.filter(booking_id__in=bookings_list):
            if Invoice.objects.get(item_purchases=item.id).is_paid:
                raise ValidationError('One of Bookings was already paid')

    def _is_invoice_attempts_exceeded(self):
        positive_attempts = Invoice.get_positive_attempts_for_period(self.user_account)
        negative_attempts = Invoice.get_negative_attempts_for_period(self.user_account)
        if (
                positive_attempts >= 5
                or negative_attempts >= 100  # изменить!!!!
        ):
            return True
        return False
