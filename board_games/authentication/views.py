from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegistrationSerializer, MyTokenObtainPairSerializer, ProfileSerializer


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

    @swagger_auto_schema(responses={200: ProfileSerializer(many=True)})
    def get(self, request):
        return Response(data=ProfileSerializer(request.user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProfileSerializer(), responses={201: ProfileSerializer()}
    )
    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED
        )