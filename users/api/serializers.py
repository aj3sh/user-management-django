import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings as jwt_settings

User = get_user_model()
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
	'''Serializer for User Detail'''

	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'email', 'password', 'is_admin', 'is_superuser')

	def save(self, *args, **kwargs):
		user = super().save(*args, **kwargs)
		if 'password' in self.validated_data:
			user.set_password(self.validated_data['password'])
			user.save(update_fields=['password'])
		return user
	

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


class UserPasswordChangeSerializer(serializers.Serializer):
	'''
	This serializer is used to update the current user's password
	'''
	current_password = serializers.CharField(required=True, write_only=True)
	new_password = serializers.CharField(required=True, write_only=True)
	confirm_password = serializers.CharField(required=True, write_only=True)

	def get_user(self):
		# checking if request exists in serializer context
		if 'request' not in self.context:
			raise Exception('Request object not found in serializes context.')
		
		# getting user
		return self.context['request'].user

	def validate_current_password(self, data):
		'''
		validates if current password is correct
		raises validation error if fails
		'''
		user = self.get_user()
		if not user.check_password(data):
			raise serializers.ValidationError('Please enter a correct password.')
		return data

	def validate_new_password(self, data):
		'''
		validates if new password is equal to the confirmation password
		raises validation error if fails
		'''
		new_password = self.initial_data.get('new_password')
		confirm_password = self.initial_data.get('confirm_password')
		if new_password != confirm_password:
			raise serializers.ValidationError('Password confirmation failed.')
		return data

	def save(self, *_, **__):
		new_password = self.validated_data.get('confirm_password')
		user = self.get_user()
		user.set_password(new_password)
		user.save(update_fields=['password'])
		logger.debug('Changing password of user {}.'.format(user))
		return None