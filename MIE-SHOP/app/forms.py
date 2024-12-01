from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustoUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter User Email'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))
    class meta:
        model=User
        fields=['username','email','password1','password2']