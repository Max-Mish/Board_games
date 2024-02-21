from django.contrib.auth.models import BaseUserManager, Group

from .services import GroupsService


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        GroupsService().create_update_groups()
        user_group = Group.objects.get(name='User')
        user.groups.add(user_group)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
