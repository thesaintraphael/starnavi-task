from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("login/", views.UserLoginAPIView.as_view(), name="login"),
    path("verify-email/", views.VerifyEmailAPIView.as_view(), name="verify-email"),
    path("activity/", views.UserActivityAPIView.as_view(), name="activity"),
]
