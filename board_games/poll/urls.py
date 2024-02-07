from django.urls import path

from .views import QuestionAPIView

app_name = 'poll'
urlpatterns = [
    path('poll/question/', QuestionAPIView.as_view(), name='question')
]
