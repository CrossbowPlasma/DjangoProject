from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Remember me')

class SignUpform(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
        labels = {'email':'Email',}
