from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from mandala_shop.models import DeliveryAddress


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
