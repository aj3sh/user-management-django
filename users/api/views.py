import logging

from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views

from .permissions import IsSuperuserOrAdmin
from .serializers import UserPasswordChangeSerializer, UserSerializer, UserTokenObtainSerializer, UserTokenRefreshSerializer

User = get_user_model()
logger = logging.getLogger(__name__)

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

class UserProfileView(RetrieveUpdateAPIView):
	'''
	View for getting authenticated user detail.
	'''
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated,)

	def get_serializer(self, *args, **kwargs):
		# getting serializer
		serializer = super().get_serializer(*args, **kwargs)
		
		# removing password field
		serializer.fields.pop('password')
		
		# making is_admin and is_superuser as a readonly field
		serializer.fields['is_admin'].read_only = True
		serializer.fields['is_superuser'].read_only = True

		# making first name and last name as required field
		serializer.fields['first_name'].required = True
		serializer.fields['last_name'].required = True

		# returning serializer
		return serializer

	def get_object(self):
		# current current user to the profile view
		if not hasattr(self, 'object'):
			self.object = self.request.user
			if self.request.method == 'GET':
				logger.debug('Retrieving user profile of {}.'.format(self.object))
		return self.object

class UserPasswordChangeAPIView(GenericAPIView):
	serializer_class = UserPasswordChangeSerializer
	permission_classes = (IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=200,)
		

# User CRUD for Admin

class UserListCreateAPIView(ListCreateAPIView):
	'''Views to list and create user'''
	permission_classes = (IsAuthenticated, IsSuperuserOrAdmin,)
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
	'''Views to retrieve, update, and delete user'''
	permission_classes = (IsAuthenticated, IsSuperuserOrAdmin,)
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_serializer(self, *args, **kwargs):
		# removing password field
		serializer = super().get_serializer(*args, **kwargs)
		serializer.fields.pop('password')
		return serializer