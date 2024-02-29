from datetime import timedelta, datetime

from django.db.models import Count

from game.models import GameItem
from game.serializers import DatesCheckResponseSerializer


def get_all_dates(date_period: list) -> list:
    date_start, date_end = [datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z").date() for date in date_period]
    return [date_start + timedelta(days=i) for i in range((date_end - date_start).days + 1)]


def get_available_game_items(game_id, dates: list):
    game_items = GameItem.objects.filter(game_id=game_id)
    available_game_items = game_items.exclude(booked_dates__date__in=dates).annotate(
        num_booked_dates=Count('booked_dates')).filter(num_booked_dates=0)
    return available_game_items


def pack_response_serializer(items, amount):
    items_length = len(items)

    dates_check_status = items_length >= amount
    dates_check_message = (
        "There are no available games for these dates." if items_length == 0
        else f"There are only {items_length} available games for these dates." if items_length < amount
        else "There are available games for these dates."
    )
    available_items_ids = [item.id for item in items[:amount]]

    serializer = DatesCheckResponseSerializer(data={
        'dates_check_status': dates_check_status,
        'message': dates_check_message,
        'items_ids': available_items_ids
    })
    serializer.is_valid(raise_exception=True)
    return serializer.data
