from django import forms
from .models import Members,Spendings,Shares
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MembersForm(forms.ModelForm):
    class Meta:
        model=Members
        fields=['name']
        

class SpendingsForm(forms.ModelForm):
    class Meta:
        model=Spendings
        fields='__all__'
        exclude=['user']
class SharesForm(forms.ModelForm):
    class Meta:
        model=Shares
        fields='__all__'
        exclude=['spends']
        
class User_registerForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        

        