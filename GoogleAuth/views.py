import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from common.response import error_response, success_response


class GoogleLoginView(APIView):
    def get(self, request):
        # Extract the authorization code from the URL parameters (query params)
        code = request.GET.get("code")
        if not code:
            return error_response(
                "Authorization code not provided", code=status.HTTP_400_BAD_REQUEST
            )

        # Prepare the request to exchange the code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8000/complete/google/",  # Ensure this matches what is registered in Google Developer Console
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        }

        try:
            # Send POST request to exchange authorization code for tokens
            response = requests.post(token_url, data=data)
            response.raise_for_status()  # Raise an exception for 4xx/5xx responses
            tokens = response.json()

            # Retrieve user info from Google using the access token
            user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            user_info_response = requests.get(user_info_url, headers=headers)
            user_info_response.raise_for_status()
            user_info = user_info_response.json()

            # Check if the user has provided email
            email = user_info.get("email")
            if not email:
                return error_response(
                    "Email not provided by Google", code=status.HTTP_400_BAD_REQUEST
                )

            # Create or get the user in the database using your custom User model
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "name": user_info.get("name"),
                    "tc": True,  # Set tc (terms and conditions) to True by default
                },
            )

            # Generate JWT token using simplejwt
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return the tokens in the success response
            return success_response(
                message="Google login successful",
                data={
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                },
            )

        except requests.exceptions.HTTPError as http_err:
            return error_response(
                f"HTTP error occurred: {http_err}", code=status.HTTP_400_BAD_REQUEST
            )
        except requests.exceptions.RequestException as req_err:
            return error_response(
                f"Request error occurred: {req_err}", code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as err:
            return error_response(
                f"An error occurred: {err}", code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
