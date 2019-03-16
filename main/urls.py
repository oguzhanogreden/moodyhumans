from django.urls import include, path

from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about", TemplateView.as_view(template_name="main/about.html"), name="about"),
    path("accounts/profile", views.ProfileView.as_view(), name="profile"),
    path("accounts/signup", views.SignupFormView.as_view(), name="signup"),
    path("accounts/openhumans/complete", views.OpenHumansAuthCompleteView.as_view()),
    path(
        "accounts/openhumans/authenticate",
        views.OpenHumansAuthStartView.as_view(),
        name="oh_auth",
    ),
    path(
        "accounts/openhumans/upload",
        views.OpenHumansUploadView.as_view(),
        name="oh_upload",
    ),
    path(
        "accounts/openhumans/upload_complete",
        views.OpenHumansUploadCompleteView.as_view(),
        name="oh_upload_complete",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]

