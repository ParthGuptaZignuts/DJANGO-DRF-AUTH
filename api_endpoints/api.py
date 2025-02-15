from django.urls import path
from authentication.views import UserRegistrationView,UserLoginView

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
]
