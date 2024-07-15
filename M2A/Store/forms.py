from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Juego


class juegoForm(ModelForm):
    class Meta:
        model = Juego
        fields= "__all__"

class customLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))