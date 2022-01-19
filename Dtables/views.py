from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'Dtables/home.html',{})

def user_login(request):
    return render(request,'Dtables/login.html',{})

def user_signup(request):
    return render(request,'Dtables/signup.html',{})