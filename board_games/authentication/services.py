from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenExt(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super(RefreshTokenExt, cls).for_user(user)
        token["user_id"] = user.pk
        token["username"] = user.username
        token["email"] = user.email
        return token


class GroupsService:
    permissions_codenames = {
        'users': {
            'view_profile_info', 'view_category', 'view_description', 'view_game',
            'add_choice', 'change_choice', 'delete_choice', 'view_choice',
            'add_question', 'change_question', 'delete_question', 'view_question',
            'add_booking', 'view_booking',
            'add_vote', 'change_vote', 'delete_vote', 'view_vote'
        },
        'moderators': {
            'view_profile_info',
            'add_category', 'change_category', 'delete_category', 'view_category',
            'add_description', 'change_description', 'delete_description', 'view_description',
            'add_game', 'change_game', 'delete_game', 'view_game',
            'add_choice', 'change_choice', 'delete_choice', 'view_choice',
            'add_question', 'change_question', 'delete_question', 'view_question',
            'add_booking', 'change_booking', 'delete_booking', 'view_booking', 'view_filtered_booking',
            'add_vote', 'change_vote', 'delete_vote', 'view_vote'
        }
    }

    @classmethod
    def create_update_group(cls, group_name, group_permissions_codenames):
        group, created = Group.objects.get_or_create(name=group_name)
        group_permissions = Permission.objects.filter(codename__in=group_permissions_codenames)
        group.permissions.add(*group_permissions)

    @classmethod
    def create_update_groups(cls):
        cls.create_update_group('User', cls.permissions_codenames['users'])
        cls.create_update_group('Moderator', cls.permissions_codenames['moderators'])
