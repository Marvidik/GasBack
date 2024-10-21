
from django.urls import path
from .views import login,register,get_last_login

urlpatterns = [
    path("login/", login,name="login"),
    path("register",register,name="register"),
    path("last_login",get_last_login,name="last_login")
]
