from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.sign_up_user, name="signup"),
    path("login/", views.log_in_user, name="login"),
    path("logout/", views.log_out_user, name="logout"),
]
