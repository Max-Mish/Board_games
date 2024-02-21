from decimal import Decimal, ROUND_HALF_DOWN

import rollbar
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404
from environs import Env
from rest_framework.response import Response
from yookassa import Configuration, Payment
from yookassa.client import ApiClient
from yookassa.domain.common import HttpVerb

from purchase.models import Invoice
from .models import Account, BalanceChange, PaymentCommission

env = Env()
env.read_env()
Configuration.account_id = env.int('SHOP_ACCOUNT_ID')
Configuration.secret_key = env.str('SHOP_SECRET_KEY')


def payment_acceptance(response):
    try:
        table = BalanceChange.objects.get(
            id=response['object']['metadata']['table_id'],
        )
    except ObjectDoesNotExist:
        payment_id = response['object']['id']
        rollbar.report_message(
            f"Can't get table for payment id {payment_id}",
            'warning',
        )
        return False

    if response['event'] == 'payment.succeeded':
        table.is_accepted = True
        table.save()
        Account.add_change_balance_method(
            pk=response['object']['metadata']['user_id'],
            amount=Decimal(response['object']['income_amount']['value']),
            operation_type='DEPOSIT'
        )
    elif response['event'] == 'payment.canceled':
        table.delete()

    return True


class PaymentCalculation:
    TWO_PLACES = Decimal(10) ** -2

    def __init__(self, payment_type, payment_service, payment_amount):
        self.payment_type = payment_type
        self.payment_service = payment_service
        self.payment_amount = payment_amount
        self.key_cache = f'unique_key_{payment_service}_{payment_type}'

    def calculate_payment_with_commission(self) -> Decimal:
        commission = self._get_commission_percent()
        return (self.payment_amount * (1 / (1 - commission / 100))).quantize(
            self.TWO_PLACES,
            ROUND_HALF_DOWN,
        )

    def calculate_payment_without_commission(self) -> Decimal:
        commission = self._get_commission_percent()
        return (self.payment_amount * ((100 - commission) / 100)).quantize(
            self.TWO_PLACES,
            ROUND_HALF_DOWN,
        )

    def _get_commission_percent(self) -> Decimal:
        if result := cache.get(self.key_cache):
            return result

        payment_commission = get_object_or_404(
            PaymentCommission,
            payment_type=self.payment_type,
            payment_service=self.payment_service,
        )

        cache.set(self.key_cache, payment_commission.commission)
        return payment_commission.commission


def request_balance_deposit_url(request, balance_increase_data):
    user_account, _ = Account.objects.get_or_create(user_uuid=balance_increase_data['user_uuid'])
    amount = balance_increase_data['amount']
    value = amount['value']
    currency = amount['currency']

    balance_change = BalanceChange.objects.create(
        account_id=user_account,
        amount=value,
        is_accepted=False,
        operation_type='DEPOSIT',
    )

    value_with_commission = PaymentCalculation(
        payment_type=balance_increase_data['payment_type'],
        payment_service=balance_increase_data['payment_service'],
        payment_amount=value,
    ).calculate_payment_with_commission()

    payment = Payment.create({
        'amount': {
            'value': value_with_commission,
            'currency': currency,
        },
        'payment_method_data': {
            'type': balance_increase_data['payment_type'],
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': request.build_absolute_uri(
                f'/payment_accounts/callback?purchase={balance_change.pk}_'),
        },
        'metadata': {
            'table_id': balance_change.pk,
            'user_id': user_account.pk,
        },
        'capture': True,
        'refundable': False,
        'description': 'Пополнение на ' + str(value),
    })

    return payment.confirmation.confirmation_url


class YookassaService:
    def __init__(self, yookassa_response):
        self.yookassa_response = yookassa_response

    def handel_payment_response(self):
        parsed_data = self.parse_response()

        if parsed_data is None:
            return
        if self.yookassa_response['event'] == 'payment.canceled':
            del parsed_data['balance_object']
            return

        if 'invoice' in parsed_data:
            if parsed_data['invoice'] is not None:
                parsed_data['invoice'].is_paid = True
                parsed_data['invoice'].save()
        return parsed_data

    def parse_response(self):
        payment_body = self.yookassa_response['object_']
        payment_event = self.yookassa_response['event']
        payer_account = Account.objects.get(pk=int(payment_body.get('metadata')['account_id']))
        balance_change_object = BalanceChange.objects.get(pk=int(payment_body.get('metadata')['balance_change_id']))

        response_data = {
            'account': payer_account,
            'balance_object': balance_change_object,
            'income_amount': payment_body.get('income_amount')['value'],
        }
        if (
                'invoice_id' not in payment_body['metadata']
                or payment_event == 'payment.canceled'
        ):
            return response_data

        invoice = Invoice.objects.get(pk=payment_body['metadata']['invoice_id'])
        response_data['invoice'] = invoice
        return response_data


def check_yookassa_response(yookassa_data, yookassa_status):
    payment_id = yookassa_data.get('id_')
    if payment_id is None:
        return False

    client = ApiClient()
    base_path = '/payments'

    path = base_path + '/' + str(payment_id)
    response = client.request(HttpVerb.GET, path)

    if str(payment_id) != response.get('id'):
        rollbar.report_message(
            'Request ID is not valid',
            'warning',
        )
        return Response(404)

    if yookassa_status != response.get('status'):
        rollbar.report_message(
            'Status is not valid',
            'warning',
        )
        return Response(404)

    if (str(yookassa_data.get('income_amount').get('value')) != response.get('income_amount').get('value')) or \
            (yookassa_data.get('income_amount').get('currency') != response.get('income_amount').get('currency')) or \
            (str(yookassa_data.get('amount').get('value')) != response.get('amount').get('value')) or \
            (yookassa_data.get('amount').get('currency') != response.get('amount').get('currency')):
        rollbar.report_message(
            'Amount is not valid',
            'warning',
        )
        return Response(404)

    if (str(yookassa_data.get('metadata').get('account_id')) != response.get('metadata').get('user_id')) or \
            (str(yookassa_data.get('metadata').get('balance_change_id')) != response.get('metadata').get('table_id')):
        rollbar.report_message(
            'Metadata is not valid',
            'warning',
        )
        return Response(404)

    return True


def add_to_db_balance_change(parsed_data):
    balance_change_object = parsed_data['balance_object']
    amount = Decimal(parsed_data['income_amount'])
    with transaction.atomic():
        balance_change_object.is_accepted = True
        balance_change_object.amount = amount
        balance_change_object.save()

        Account.add_change_balance_method(
            pk=balance_change_object.account_id.pk,
            amount=Decimal(amount),
            operation_type='DEPOSIT'
        )


def proceed_payment_response(income_data, payment_service):
    parsed_data = None
    if payment_service == 'yookassa':
        parsed_data = YookassaService(income_data).handel_payment_response()
    if parsed_data is None:
        return False
    if 'invoice' not in parsed_data:
        add_to_db_balance_change(parsed_data)
    else:
        balance_change_object = parsed_data['balance_object']
        balance_change_object.is_accepted = True
        balance_change_object.save()
    return True
