from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, FileInput

from .models import Profile
from account.models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'id': 'login', 'placeholder': 'login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'id': 'password', 'placeholder': 'password'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'user': TextInput(attrs={'class':'input','placeholder':'user'}),
            'photo': FileInput(attrs={'class': 'input', 'placeholder':'photo'}),
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'phone'}),
        }



