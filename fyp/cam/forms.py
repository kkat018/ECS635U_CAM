from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['name', 'email',
                  'phone_number', 'password1', 'password2']
