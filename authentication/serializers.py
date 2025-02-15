from rest_framework import serializers
from authentication.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'confirm_password', 'tc']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    confirm_password = attrs.get('confirm_password')
    if password != confirm_password:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name', 'tc']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, 
        style={'input_type': 'password'}, 
        write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, 
        style={'input_type': 'password'}, 
        write_only=True
    )

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return attrs  

    def save(self, **kwargs):
        """Explicitly update the user's password"""
        user = self.context.get('user')
        user.set_password(self.validated_data['password'])
        user.save()
        return user