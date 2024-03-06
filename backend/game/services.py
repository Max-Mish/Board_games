from datetime import timedelta, datetime

from django.db.models import Count

from game.models import GameItem, BookedDate
from game.serializers import DatesCheckResponseSerializer


def get_all_dates(date_period: list) -> list:
    date_start, date_end = [datetime.strptime(date, "%a %b %d %Y").date() for date in date_period]
    return [date_start + timedelta(days=i) for i in range((date_end - date_start).days + 1)]


def get_available_game_items(game_id, dates: list):
    game_items = GameItem.objects.filter(game_id=game_id)
    available_game_items = []
    for game_item in game_items:
        booked_dates = BookedDate.objects.filter(gameitem=game_item)
        booked_dates_list = list(booked_dates.values_list('date', flat=True))
        if not any(date in dates for date in booked_dates_list):
            available_game_items.append(game_item)
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


def get_disabled_dates(game_id):
    total_count = GameItem.objects.filter(game_id=game_id).count()

    fully_booked_dates = BookedDate.objects.filter(
        gameitem__game_id=game_id
    ).annotate(
        booked_count=Count('gameitem')
    ).filter(
        booked_count=total_count
    )

    return list(fully_booked_dates.values_list('date', flat=True))
