from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegistrationSerializer, MyTokenObtainPairSerializer, ProfileSerializer, JWTRefreshSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        request_body=RegistrationSerializer(), responses={201: RegistrationSerializer()}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ProfileAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)

    @swagger_auto_schema(responses={200: ProfileSerializer(many=True)})
    def get(self, request):
        request.auth.verify()
        user_id = request.auth.get("user_id")
        return Response(data=ProfileSerializer(request.user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProfileSerializer(), responses={201: ProfileSerializer()}
    )
    def patch(self, request):
        serializer = ProfileSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # instance = request.user
        # validated_data = serializer.data
        #
        # user_changes = ('password', 'email', 'cover_photo', 'is_active')
        # admin_changes = ('username', 'is_staff', 'is_superuser')
        #
        # for key, value in validated_data.items():
        #     if key in user_changes or (key in admin_changes and instance.is_superuser):
        #         if key == 'password' and value is not None:
        #             instance.set_password(value)
        #         else:
        #             setattr(instance, key, value)
        #     else:
        #         raise generics.ValidationError('This field can not be changed')
        #
        # instance.save()
        serializer.save()

        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED
        )


class JWTRefreshView(TokenRefreshView):
    serializer_class = JWTRefreshSerializer
