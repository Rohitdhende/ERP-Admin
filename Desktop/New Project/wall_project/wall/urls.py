from django.urls import path,re_path
from . views import *
urlpatterns = [
    path('',login_render,name="login_render"),
    path('activate/<uidb64>/<token>/',email_activation_login,name="email_activation_login"),
    path('register/',register_render,name="register_render"),
    path('register_ajax/',RegisterAPIView.as_view(),name="registration"),
    path('login_ajax/',LoginAPIView.as_view(),name="Login"),
    path('main_page/',MainPageAPIView.as_view(),name="Index"),

    ]
