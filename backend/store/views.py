from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response

from store.models import Store
from store.serializers import StoreResponseSerializer


class StoresAPIView(generics.GenericAPIView):
    @swagger_auto_schema(responses={200: StoreResponseSerializer(many=True)})
    def get(self, request):
        queryset = Store.objects.all().order_by('-id')
        return Response(data=StoreResponseSerializer(queryset, many=True).data,
                        status=status.HTTP_200_OK)
