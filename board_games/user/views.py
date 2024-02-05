from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from .models import User
from .serialiers import UserSerializer, UserRequestShortSerializer, UserResponseShortSerializer


class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')


class UserShortListViewSet(generics.GenericAPIView):
    @swagger_auto_schema(responses={200: UserResponseShortSerializer(many=True)})
    def get(self, request):
        queryset = User.objects.all().order_by('-date_joined')
        return Response(data=UserResponseShortSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserRequestShortSerializer(), responses={201: UserResponseShortSerializer()}
    )
    def post(self, request):
        serializer = UserRequestShortSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User(question_text=data['username'], picture=data['password'])
        user.save()
        return Response(
            data=UserResponseShortSerializer(user).data, status=status.HTTP_201_CREATED
        )
