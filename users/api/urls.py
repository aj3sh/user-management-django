from django.urls import path
from rest_framework_simplejwt.views import token_blacklist

from . import views

urlpatterns = [

    # auth
    path('login', views.UserLoginAPIView.as_view(), name='login'),
    path('token-refresh', views.UserLoginTokenRefreshAPIView.as_view(), name='token-refresh'),
    path('logout', token_blacklist, name='logout'),

    # user profile
    path('profile', views.UserProfileView.as_view(), name='profile'),
]