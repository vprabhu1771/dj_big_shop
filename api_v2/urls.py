from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api_v2.views import UserCreateAPIView, CustomAuthToken, CurrentUserView, LogoutAPIView

urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name='create'),

    # Login Type 1
    path('token', obtain_auth_token, name='api_token_auth'),

    # Login Type 2
    path('login', CustomAuthToken.as_view(), name='custom_api_token_auth'),

    path('user', CurrentUserView.as_view(), name='current-user'),

    # Logout
    path('logout', LogoutAPIView.as_view(), name='logout'),
]