from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm

# register view
from django.views import View
from django.contrib.auth import login

# Create your views here.

class UserLoginView(LoginView):
    template_name= "users/login.html"
    next_page = 'home'

class UserLogoutView(LogoutView):
    next_page = 'login'
    
    

class UserRegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "users/register.html", {"form": form})



# from django.core.mail import send_mail

# send_mail(
#     subject="Test Email",
#     message="Email system is working",
#     from_email=None,
#     recipient_list=["your_email@gmail.com"],
# )


    
