from django.urls import path

from .views import QuestionListViewSet

urlpatterns = [
    path('poll/question/', QuestionListViewSet.as_view())
]
