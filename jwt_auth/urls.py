from django.contrib import admin
from django.urls import include, path

from authentication.views import check_server
from GoogleAuth.views import GoogleLoginView

# Admin panel URL configuration and Server Health check endpoint
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", check_server, name="check_server"),
]

# API endpoint configurations
urlpatterns += [
    path("api/", include("api_endpoints.api")),
]

# Authentication and social login for Sigin With Google URLs
urlpatterns += [
    path("auth/", include("social_django.urls")),
    path("complete/google/", GoogleLoginView.as_view(), name="google-login"),
]
