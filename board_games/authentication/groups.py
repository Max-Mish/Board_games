import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "board_games.settings")

import django

django.setup()

from django.contrib.auth.models import Group, Permission


def create_update_user_group():
    users_group, created = Group.objects.get_or_create(name='Users')
    users_permissions_codenames = [
        'view_profile_info',
        'view_category', 'view_description', 'view_game',
        'add_choice', 'change_choice', 'delete_choice', 'view_choice',
        'add_question', 'change_question', 'delete_question', 'view_question',
        'add_booking', 'view_booking',
        'add_vote', 'change_vote', 'delete_vote', 'view_vote'
    ]

    users_permissions = Permission.objects.filter(codename__in=users_permissions_codenames)
    for permission in users_permissions:
        users_group.permissions.add(permission)


def create_update_moderator_group():
    moderators_group, created = Group.objects.get_or_create(name='Moderators')
    moderators_permissions_codenames = [
        'view_profile_info',
        'add_category', 'change_category', 'delete_category', 'view_category',
        'add_description', 'change_description', 'delete_description', 'view_description',
        'add_game', 'change_game', 'delete_game', 'view_game',
        'add_choice', 'change_choice', 'delete_choice', 'view_choice',
        'add_question', 'change_question', 'delete_question', 'view_question',
        'add_booking', 'change_booking', 'delete_booking', 'view_booking', 'view_filtered_booking',
        'add_vote', 'change_vote', 'delete_vote', 'view_vote'
    ]

    moderators_permissions = Permission.objects.filter(codename__in=moderators_permissions_codenames)
    for permission in moderators_permissions:
        moderators_group.permissions.add(permission)


if __name__ == '__main__':
    create_update_user_group()
    create_update_moderator_group()
