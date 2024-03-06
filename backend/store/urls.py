from django.urls import path

from store.views import StoresAPIView

app_name = 'store'
urlpatterns = [
    path('', StoresAPIView.as_view(), name='stores'),
]
