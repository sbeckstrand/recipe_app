# recipes/views.py

import json
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeForm, LoginForm, IngredientForm


def index(request):
    recipes = Recipe.objects.order_by('-pk')[:5]
    return render(request, 'index.html', {'recipes': recipes, 'title': 'Home'})

def recipe_all(request):
    recipes = Recipe.objects.order_by('-pk').all()
    return render(request, 'recipes/recipe_all.html', {'recipes': recipes, 'title': 'Recipes'})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {
        'recipe': recipe,
        'title': recipe.title,
        'ingredients': recipe.ingredients.split('\n'),
        'instructions': recipe.instructions.split('\n')
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
        'title': "New Recipe",
        'sections': ['ingredient', 'instruction']
    }
    return render(request, 'recipes/recipe_edit.html', context)

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    
    context = {
        'recipe': recipe,
        'form': form,
        'title': f'{ recipe.title } - Edit',
        'sections': ['ingredient', 'instruction']
    }
    return render(request, 'recipes/recipe_edit.html', context)

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('recipe_all')

def recipe_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query')

        if search_query:
            recipes = Recipe.objects.filter(title__icontains=search_query)
        else:
            recipes = Recipe.objects.all()
        
        context = {
            'recipes': recipes,
            'search_query': search_query,
            'title': 'Search Results'
        }
        
        return render(request, 'recipes/recipe_all.html', context)
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or any desired page after login
                return redirect("/")  # Replace 'success-page' with your URL name
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a specific page after logout (e.g., home page)
    return redirect('/')  # Replace 'home' with your desired URL name

def test_view(request):
    if request.method == 'POST':
        # Process the submitted form data here
        ingredient_data = {}
        count = 0
        for key, val  in request.POST.items():
            if 'dynamic-field-ingredient' in key:
                ingredient_data[count] = val
                count += 1
        ingredient_json = json.dumps(ingredient_data)
       


        try:
            json.loads(ingredient_json)
            valid = True
        except ValueError as e:
            valid = False
    
        if valid: 
            ingredients = ingredient_json
            return redirect("/recipes/")

        return redirect("/")
        # Do something with the form data
        # Redirect or render a response
    else:
        # Render the initial form for GET requests
        context = {
            'sections': ['ingredient', 'instruction']
        }
        return render(request, 'recipe_form.html', context)