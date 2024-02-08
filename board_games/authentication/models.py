from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_photo = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     is_superuser = request.user.is_superuser
    #
    #     if (
    #             not is_superuser
    #             and obj is not None
    #             and obj == request.user
    #     ):
    #         form.base_fields['is_superuser'].disabled = True
    #         form.base_fields['is_active'].disabled = True
    #         form.base_fields['is_staff'].disabled = True
    #         form.base_fields['created_at'].disabled = True
    #
    #     return form

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            (
                "view_profile_info",
                "Can view profile information"
            ),
        ]
