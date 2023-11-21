# recipes/forms.py

from django import forms
from django.forms import formset_factory
from django.contrib.auth.forms import AuthenticationForm
from .models import Recipe

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'description')

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))