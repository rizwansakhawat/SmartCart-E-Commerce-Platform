from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
# register view
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class UserLoginView(LoginView):
    template_name= "users/login.html"
    next_page = 'home'

class UserLogoutView(LogoutView):
    next_page = 'login'
    
class UserRegisterView(View):
    
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'users/register.html', {"form":form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, 'users/register.html', {"form":form})


    
