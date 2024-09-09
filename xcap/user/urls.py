from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("change-email/", views.change_email, name="change_email"),
    path("change-password/", views.change_password, name="change_email"),
    path("get-user/", views.get_user, name="get_user"),
]
