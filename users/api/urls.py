from django.urls import path
from rest_framework_simplejwt.views import token_blacklist

from . import views

urlpatterns = [

    # auth
    path('login', views.UserLoginAPIView.as_view(), name='login'),
    path('token-refresh', views.UserLoginTokenRefreshAPIView.as_view(), name='token-refresh'),
    path('logout', token_blacklist, name='logout'),

    # user profiles
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('change-password', views.UserPasswordChangeAPIView.as_view(), name='change-password'),

    # users crud
    path('', views.UserListCreateAPIView.as_view(), name='users-list-create'),
    path('<uuid:pk>', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='users-retrieve-update-destroy'),
    
]