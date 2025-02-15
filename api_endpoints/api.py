from django.urls import path
from authentication.views import UserRegistrationView,UserLoginView,UserProfileView

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
]

urlpatterns += [
  path('user/profile/', UserProfileView.as_view(), name='user-profile'),
]