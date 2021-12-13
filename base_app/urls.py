from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="base_app/login.html",
        ),
        name="login",
    ),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="base_app/reset_password.html",
            email_template_name="base_app/password_reset_email.html",
            subject_template_name="base_app/password_reset_subject.txt",
            success_url=reverse_lazy("base_app:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="base_app/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="base_app/password_reset_confirm.html",
            success_url=reverse_lazy("base_app:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="base_app/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]
