from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings as jwt_settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	'''Serializer for User Detail'''
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'email', )

class UserTokenExtraDataMixin:
	'''
	This mixins helps providing extra details in the authentication response.
	'''
	def validate(self, attrs):
		data = super().validate(attrs)

		# extra fields
		data['expires_in'] = jwt_settings.ACCESS_TOKEN_LIFETIME
		if hasattr(self, 'user'):
			data['user'] = UserSerializer(self.user).data

		return data

class UserTokenObtainSerializer(UserTokenExtraDataMixin, TokenObtainPairSerializer):
	pass
	
class UserTokenRefreshSerializer(UserTokenExtraDataMixin, TokenRefreshSerializer):
	pass
