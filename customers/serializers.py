from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from .models import User, Address


class RegisterSerializer(serializers.ModelSerializer):
	# password = serializers.CharField(max_length=68, min_length=6, write_only=True)
	class Meta:
		model = User
		fields = ['email', 'username', 'password']

	# def validate(self, attrs):
	#     email = attrs.get('email', '')
	#     username = attrs.get('username', '')
	#     if not username.isalnum():
	#         raise serializers.ValidationError(
	#             self.default_error_messages)
	#     return attrs

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=255, min_length=3)
	password = serializers.CharField(max_length=68, min_length=6, write_only=True)
	tokens = serializers.SerializerMethodField()

	def get_tokens(self, obj):
		user = User.objects.get(username=obj['username'])
		return {
			'refresh': user.tokens()['refresh'],
			'access': user.tokens()['access']
		}

	class Meta:
		model = User
		fields = ['username', 'password', 'tokens']

	def validate(self, attrs):
		username = attrs.get('username', '')
		password = attrs.get('password', '')
		user = authenticate(username=username, password=password)

		if user is None:
			raise AuthenticationFailed('Invalid credentials, try again')

		if not user.is_active:
			raise AuthenticationFailed('Account disabled, contact admin')

		attrs['user'] = user
		return attrs


# class LogoutSerializer(serializers.Serializer):
# 	refresh = serializers.CharField()
#
# 	def validate(self, attrs):
# 		self.token = attrs['refresh']
# 		return attrs
#
# 	def save(self, **kwargs):
# 		try:
# 			RefreshToken(self.token).blacklist()
# 		except TokenError:
# 			self.fail('bad_token')


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields =['first_name', 'last_name', 'email', 'phone_number']
