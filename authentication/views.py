from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from api_endpoints.response import success_response, error_response
from api_endpoints.renderers import UserRenderer
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer , UserChangePasswordSerializer , SendPasswordResetEmailSerializer , UserPasswordResetSerializer

from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def check_server(request):
    """
    A simple view to check if the server is working.
    """
    return success_response(message="Server is working!")


def get_tokens_for_user(user):
    """
    Generates JWT tokens for an authenticated user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    """
    Handles user registration.
    """
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return success_response(
                message="Registration Successful",
                data={'token': token},
                code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Registration Failed",
            errors=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        )


class UserLoginView(APIView):
    """
    Handles user login authentication.
    """
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return success_response(
                    message="Login Successful",
                    data={'token': token},
                    code=status.HTTP_200_OK
                )

            return error_response(
                message="Invalid Credentials",
                errors={"non_field_errors": ["Email or Password is incorrect"]},
                code=status.HTTP_401_UNAUTHORIZED
            )

        return error_response(
            message="Login Failed",
            errors=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(APIView):
    """
    Handles retrieving the authenticated user's profile.
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return success_response(
            message="User profile fetched successfully",
            data=serializer.data,
            code=status.HTTP_200_OK
        )
    
class UserChangePasswordView(APIView):
    """
    Handles user password change.
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="Password changed successfully",
                code=status.HTTP_200_OK
            )
        return error_response(
            message="Password change failed",
            errors=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        )


class SendPasswordResetEmailView(APIView):
    """
    Handles sending password reset email.
    """
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(
            message="Password reset link sent. Please check your email.",
            code=status.HTTP_200_OK
        )

class UserPasswordResetView(APIView):
    """
    Handles resetting the user password.
    """
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return success_response(
            message="Password reset successfully",
            code=status.HTTP_200_OK
        )

class UserLogoutView(APIView):
    """
    Handles user logout by blacklisting the refresh token.
    """
    
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer] 

    def post(self, request, format=None):
        refresh_token = request.data.get("refresh")
        print(refresh_token)

        if not refresh_token:
            return error_response(
                message="Refresh token is required",
                errors={"refresh": "This field is required."},
                code=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh_token_obj = RefreshToken(refresh_token)
            print(refresh_token_obj)
            refresh_token_obj.blacklist() 

            return success_response(
                message="Logout successfully",
                code=status.HTTP_200_OK
            )

        except Exception as e:
            return error_response(
                message="Invalid or expired token.",
                errors={"non_field_errors": "Invalid token."},
                code=status.HTTP_401_UNAUTHORIZED
            )