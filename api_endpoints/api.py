from django.urls import path
from authentication.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('user/reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]

urlpatterns += [
  path('user/profile/', UserProfileView.as_view(), name='user-profile'),
  path('user/changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
]