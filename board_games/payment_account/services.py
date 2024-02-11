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


def request_balance_deposit_url(balance_increase_data):
    user_account, _ = Account.objects.get_or_create(user_uuid=balance_increase_data['user_uuid'])
    amount = balance_increase_data.get('amount')
    value = amount.get('value')
    currency = amount.get('currency')

    balance_change = BalanceChange.objects.create(
        account_id=user_account,
        amount=value,
        is_accepted=False,
        operation_type='DEPOSIT',
    )

    value_with_commission = PaymentCalculation(
        payment_type=balance_increase_data.get('payment_type'),
        payment_service=balance_increase_data.get('payment_service'),
        payment_amount=value,
    ).calculate_payment_with_commission()

    payment = Payment.create({
        'amount': {
            'value': value_with_commission,
            'currency': currency,
        },
        'payment_method_data': {
            'type': balance_increase_data.get('payment_type'),
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': balance_increase_data.get('return_url'),
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


class YookassaService():
    def __init__(self, yookassa_response):
        self.yookassa_response = yookassa_response

    def handel_payment_response(self):
        parsed_data = self.parse_response()

        if parsed_data is None:
            return
        if self.yookassa_response['event'] == 'payment.canceled':
            del parsed_data['balance_object']
            return

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
            'invoice': None
        }
        if (
                'invoice_id' not in payment_body['metadata']
                or payment_event == 'payment.canceled'
        ):
            return response_data

        # invoice = Invoice.objects.get(pk=payment_body.metadata['invoice_id'])
        # response_data['invoice'] = invoice
        # return response_data


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

    if (yookassa_data.get('income_amount').get('value') != response.get('income_amount').get('value')) or \
            (yookassa_data.get('income_amount').get('currency') != response.get('income_amount').get('currency')) or \
            (yookassa_data.get('amount').get('value') != response.get('amount').get('value')) or \
            (yookassa_data.get('amount').get('currency') != response.get('amount').get('currency')):
        rollbar.report_message(
            'Amount is not valid',
            'warning',
        )
        return Response(404)

    if (yookassa_data.get('metadata').get('account_id') != response.get('metadata').get('user_id')) or \
            (yookassa_data.get('metadata').get('balance_change_id') != response.get('metadata').get('table_id')):
        rollbar.report_message(
            'Metadata is not valid',
            'warning',
        )
        return Response(404)

    return True


# {'id': '2d5b0829-000f-5000-8000-165a2ecdc84d', 'status': 'succeeded', 'amount': {'value': '414.51', 'currency': 'RUB'},
#  'income_amount': {'value': '400.00', 'currency': 'RUB'}, 'description': 'Пополнение на 400.00',
#  'recipient': {'account_id': '332026', 'gateway_id': '2190794'},
#  'payment_method': {'type': 'bank_card', 'id': '2d5b0829-000f-5000-8000-165a2ecdc84d', 'saved': False,
#                     'title': 'Bank card *4444',
#                     'card': {'first6': '555555', 'last4': '4444', 'expiry_year': '2011', 'expiry_month': '11',
#                              'card_type': 'MasterCard', 'issuer_country': 'US'}},
#  'captured_at': '2024-02-11T16:23:23.328Z', 'created_at': '2024-02-11T16:23:06.001Z', 'test': True,
#  'refunded_amount': {'value': '0.00', 'currency': 'RUB'}, 'paid': True, 'refundable': True,
#  'metadata': {'table_id': '17', 'user_id': '1'},
#  'authorization_details': {'rrn': '157261377829532', 'auth_code': '831830',
#                            'three_d_secure': {'applied': False, 'method_completed': False,
#                                               'challenge_completed': False}}}

# OrderedDict({'id_': UUID('2d5b0829-000f-5000-8000-165a2ecdc84d'),
#              'income_amount': OrderedDict({'currency': 'RUB', 'value': Decimal('400.00')}),
#              'amount': OrderedDict({'currency': 'RUB', 'value': Decimal('414.51')}),
#              'description': 'Пополнение на 400.00', 'metadata': {'account_id': 1, 'balance_change_id': 16},
#              'payment_method': 'bank_card'})


def add_to_db_payout_info(parsed_data):
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
    add_to_db_payout_info(parsed_data)
    if parsed_data['invoice'] is None:
        return True

    # execute_invoice_operations(
    #     invoice_instance=parsed_data.invoice,
    #     payer_account=parsed_data.account,
    #     decrease_amount=parsed_data.income_amount,
    # )
    #
    # return True
