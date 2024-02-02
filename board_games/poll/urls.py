from django.urls import path, include

from .views import QuestionListViewSet

urlpatterns = [
    path('question/', QuestionListViewSet.as_view())
]