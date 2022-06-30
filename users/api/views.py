from cgitb import reset
from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt import views as jwt_views

from .serializers import UserSerializer, UserTokenObtainSerializer, UserTokenRefreshSerializer

User = get_user_model()

# Auth Views

class UserLoginAPIView(jwt_views.TokenObtainPairView):
	'''
	Views to login user.
	Accepts email and password to authenticate.
	Returns access token, refresh token, token expiry time, user detail.
	'''
	serializer_class = UserTokenObtainSerializer

class UserLoginTokenRefreshAPIView(jwt_views.TokenRefreshView):
	'''
	Views to refresh access token.
	Accepts refresh and returns new access token with new expiry time.
	'''
	serializer_class = UserTokenRefreshSerializer


# User Profile Views

class UserProfileView(RetrieveAPIView):
	'''
	View for getting authenticated user detail.
	'''
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user