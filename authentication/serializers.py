from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from authentication.models import User
from common.email import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Includes an additional `confirm_password` field to ensure users confirm their password during registration.

    Fields:
        - email (str): User's email address.
        - name (str): User's full name.
        - password (str): User's password.
        - confirm_password (str): Confirmation of the password.
        - tc (bool): Terms and conditions agreement.

    Methods:
        - validate(attrs): Validates that `password` and `confirm_password` match.
        - create(validated_data): Creates a new user.
    """

    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "name", "password", "confirm_password", "tc"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """
        Validates that the password and confirm password fields match.
        """
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match"
            )
        return attrs

    def create(self, validate_data):
        """
        Creates and returns a new user instance.
        """
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.

    Fields:
        - email (str): User's email address.
        - password (str): User's password.
    """

    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user profile details.

    Fields:
        - id (int): Unique identifier for the user.
        - email (str): User's email address.
        - name (str): User's full name.
        - tc (bool): Terms and conditions agreement.
    """

    class Meta:
        model = User
        fields = ["id", "email", "name", "tc"]


class UserChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.

    Fields:
        - password (str): The new password.
        - confirm_password (str): Confirmation of the new password.

    Methods:
        - validate(attrs): Ensures `password` and `confirm_password` match.
        - save(): Updates the user's password.
    """

    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        """
        Validates that the password and confirm password fields match.
        """
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return attrs

    def save(self, **kwargs):
        """
        Updates the user's password and saves the user instance.
        """
        user = self.context.get("user")
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class SendPasswordResetEmailSerializer(serializers.Serializer):
    """
    Serializer for sending password reset emails.

    Fields:
        - email (str): The user's email address.

    Methods:
        - validate(attrs): Sends a password reset email if the user exists.
    """

    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        """
        Validates the email and sends a password reset link if the user exists.
        """
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = (
                f"{settings.FRONTEND_URL}/api/user/reset-password/{uid}/{token}/"
            )

            context = {"user": user, "reset_link": reset_link}

            data = {
                "subject": "Reset Your Password",
                "to_email": user.email,
                "context": context,
            }

            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("You are not a registered user")


class UserPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for resetting user password.

    Fields:
        - password (str): The new password.
        - confirm_password (str): Confirmation of the new password.

    Methods:
        - validate(attrs): Validates the reset token and updates the password.
    """

    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        """
        Validates the password reset token and updates the user's password.
        """
        try:
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password")
            uid = self.context.get("uid")
            token = self.context.get("token")

            if password != confirm_password:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match"
                )
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not Valid or Expired")
            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not Valid or Expired")
