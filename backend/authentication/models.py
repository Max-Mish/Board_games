import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_photo = models.URLField(blank=True, null=True)
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)
    refresh_token = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            (
                "view_profile_info",
                "Can view profile information"
            ),
        ]
