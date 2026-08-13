from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from .apps import UsersConfig

from . import views

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("register/pending/", TemplateView.as_view(template_name="users/pending.html"), name="registration_pending"),
    path("activate/<str:uidb64>/<str:token>/", views.ActivateView.as_view(), name="activate"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password_reset/complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
