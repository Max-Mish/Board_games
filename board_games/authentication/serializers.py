from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user_id"] = user.pk
        token['username'] = user.username
        token['email'] = user.email

        user.refresh_token = token
        user.access_token = token.access_token
        user.save()

        return token


class JWTRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh_token"])

        data = {"access_token": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh_token"] = str(refresh)
            user_id = refresh.access_token.get("user_id")
            CustomUser.objects.filter(id=user_id).update(refresh_token=str(refresh))
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'cover_photo', 'password', 'password_repeat']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        del attrs['password_repeat']
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

        # def update(self, instance, validated_data):
        #     password = validated_data.pop('password', None)
        #
        #     # user_changes = ('email', 'cover_photo', 'is_active')
        #     # admin_changes = ('is_staff', 'is_superuser')
        #
        #     # for key, value in validated_data.items():
        #     #     if key in user_changes or (key in admin_changes and instance.is_superuser):
        #     #         setattr(instance, key, value)
        #     #     else:
        #     #         raise serializers.ValidationError('This field can not be changed')
        #
        #     instance = super().update(instance, validated_data)
        #
        #     if password is not None:
        #         instance.set_password(password)
        #
        #     instance.save()
        #
        #     return instance


class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'cover_photo']

# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=255)
#     username = serializers.CharField(max_length=255, read_only=True)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     def validate(self, data):
#         email = data.get('email', None)
#         password = data.get('password', None)
#
#         if email is None:
#             raise serializers.ValidationError(
#                 'An email address is required to log in.'
#             )
#
#         if password is None:
#             raise serializers.ValidationError(
#                 'A password is required to log in.'
#             )
#
#         user = authenticate(username=email, password=password)
#
#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this email and password was not found.'
#             )
#
#         if not user.is_active:
#             raise serializers.ValidationError(
#                 'This user has been deactivated.'
#             )
#
#         return {
#             'email': user.email,
#             'username': user.username,
#             'token': user.token
#         }
#
#
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         max_length=128,
#         min_length=8,
#         write_only=True
#     )
#
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'username', 'password', 'token',)
#         read_only_fields = ('token',)
#
#     def update(self, instance, validated_data):
#         password = validated_data.pop('password', None)
#
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#
#         if password is not None:
#             instance.set_password(password)
#
#         instance.save()
#
#         return instance
