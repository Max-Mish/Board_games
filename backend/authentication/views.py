from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegistrationSerializer, MyTokenObtainPairSerializer, ProfileUpdateSerializer, \
    JWTRefreshSerializer, BlacklistRefreshSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class BlacklistRefreshView(generics.GenericAPIView):
    serializer_class = BlacklistRefreshSerializer

    def post(self, request):
        serializer = BlacklistRefreshSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        Response('Logged Out')


class JWTRefreshView(TokenRefreshView):
    serializer_class = JWTRefreshSerializer


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

    @swagger_auto_schema(responses={200: ProfileUpdateSerializer()})
    def get(self, request):
        request.auth.verify()
        return Response(data=ProfileUpdateSerializer(request.user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProfileUpdateSerializer(), responses={201: ProfileUpdateSerializer()}
    )
    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user

        user.email = data.get('email', user.email)
        user.username = data.get('username', user.username)
        user.cover_photo = data.get('cover_photo', user.cover_photo)
        password = data.get('password', user.password)
        user.set_password(password)
        user.is_active = data.get('is_active', user.is_active)

        user.save()
        return Response(
            data=ProfileUpdateSerializer(user).data, status=status.HTTP_200_OK
        )
