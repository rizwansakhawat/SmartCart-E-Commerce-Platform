from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.

class UserLoginView(LoginView):
    template_name= "users/login.html"
    next_page = 'home'

class UserLogoutView(LogoutView):
    next_page = 'login'
    
