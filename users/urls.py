from django.urls import path

from users.views import CreateUserAPIView, RetrieveUpdateUserAPIView

from rest_auth.views import LoginView, LogoutView


app_name = 'users'

urlpatterns = [
    path(
        "create/",
        CreateUserAPIView.as_view(),
        name="user-create"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="user-login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="user-logout"
    ),

    path(
        "me/",
        RetrieveUpdateUserAPIView.as_view(),
        name="user-me"
    ),
]
