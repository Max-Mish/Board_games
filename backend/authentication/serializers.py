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

        token["user_id"] = str(user.pk)
        token['username'] = user.username
        token['email'] = user.email

        user.refresh_token = token
        user.save()

        return token


class BlacklistRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh_token"])
        refresh.blacklist()
        user_id = refresh.access_token.get("user_id")
        CustomUser.objects.filter(id=user_id).update(refresh_token=None)
        return 'Logged Out'


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


class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=False,
        validators=[validate_password],
    )

    password_repeat = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    cover_photo = serializers.URLField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'cover_photo', 'password', 'is_active', 'cover_photo', 'password_repeat']

    def validate(self, attrs):
        try:
            if attrs['password'] != attrs['password_repeat']:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})

            del attrs['password_repeat']
            return attrs
        except KeyError:
            if 'password' in attrs or 'password_repeat' in attrs:
                raise serializers.ValidationError("No password repeat field.")
            else:
                return attrs


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
