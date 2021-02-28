from . import views
from django.shortcuts import redirect,render




def authenticate_user(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            return redirect("login")
    return wrapper

def un_auth_users(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return func(request,*args,**kwargs)
    return wrapper