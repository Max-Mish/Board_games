from django.core.exceptions import ValidationError
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PurchaseItemsSerializer
from .services import ItemPurchaseRequest


class PurchaseItemView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PurchaseItemsSerializer

    @swagger_auto_schema(request_body=PurchaseItemsSerializer(),
                         responses={201: 'Amount with commission returned'})
    def create(self, request, *args, **kwargs):
        serializer = PurchaseItemsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['user_uuid_from'] = request.user.pk
        if 'user_uuid_to' not in data:
            data['user_uuid_to'] = request.user.pk

        try:
            item_purchase_request = ItemPurchaseRequest(data)
        except ValidationError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as error:
            return Response(
                {'detail': str(error)},
                status=status.HTTP_404_NOT_FOUND,
            )

        response = item_purchase_request.request_items_purchase()
        return Response({'response': response}, status=status.HTTP_200_OK)
