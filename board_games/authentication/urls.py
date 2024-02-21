from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegistrationAPIView, MyTokenObtainPairView, ProfileAPIView, JWTRefreshView, BlacklistRefreshView

app_name = 'authentication'
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/blacklist', BlacklistRefreshView.as_view(), name="logout"),
    path('token/refresh/', JWTRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='auth_register'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
