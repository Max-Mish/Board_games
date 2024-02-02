from datetime import date
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from .models import Question, Choice
from .serialiers import QuestionRequestSerializer, QuestionResponseSerializer


class QuestionListViewSet(generics.GenericAPIView):
    @swagger_auto_schema(responses={200: QuestionResponseSerializer(many=True)})
    def get(self, request):
        queryset = Question.objects.all().order_by('-pub_date')
        # Choice.objects.filter(question_id=)
        return Response(data=QuestionResponseSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=QuestionRequestSerializer(), responses={201: QuestionResponseSerializer()}
    )
    def post(self, request):
        serializer = QuestionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        question = Question(question_text=data['question_text'], picture=data['picture'])
        question.save()
        return Response(
            data=QuestionResponseSerializer(question).data, status=status.HTTP_201_CREATED
        )
