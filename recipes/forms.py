# recipes/forms.py

from django import forms
from django.forms import formset_factory
from django.contrib.auth.forms import AuthenticationForm
from .models import Recipe

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'ingredients', 'instructions')

class IngredientForm(forms.Form):
    ingredient = forms.CharField(max_length=100, label="Ingredient")

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))