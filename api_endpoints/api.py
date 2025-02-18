from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,UserLogoutView

urlpatterns = [
  path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

urlpatterns += [
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('user/reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]

urlpatterns += [
  path('user/profile/', UserProfileView.as_view(), name='user-profile'),
  path('user/changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
  path('user/logout/', UserLogoutView.as_view(), name='user-logout'),
]