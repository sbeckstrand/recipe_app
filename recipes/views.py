# recipes/views.py

import json
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeForm, LoginForm


def index(request):
    recipes = Recipe.objects.order_by('-pk')[:5]
    return render(request, 'index.html', {'recipes': recipes, 'title': 'Home'})

def recipe_all(request):
    recipes = Recipe.objects.order_by('-pk').all()
    return render(request, 'recipes/recipe_all.html', {'recipes': recipes, 'title': 'Recipes'})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.prep_time == "None":
        print(recipe.prep_time)

    has_details = False
    if recipe.information != "{}":
        has_details = True

    for val in [recipe.servings, recipe.cals_per_serving, recipe.prep_time, recipe.cook_time, recipe.source]:
        if val:
            has_details = True
            break

    context = {
        'recipe': recipe,
        'title': recipe.title,
        'details': json.loads(recipe.information),
        'ingredients': json.loads(recipe.ingredients),
        'instructions': json.loads(recipe.instructions),
        'has_details': has_details,
        'locked_details': {
            'servings': { 'name': 'Yield', 'value': recipe.servings },
            'cals_per_serving': { 'name': 'Calories Per Serving', 'value': recipe.cals_per_serving },
            'prep_time': { 'name': "Prep Time", 'value': recipe.prep_time },
            'cook_time': { 'name': "Cook Time", 'value': recipe.cook_time }
        }
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)

        valid = True
        if not form.is_valid():
            valid = False
        
        cals_per_serv = request.POST.get('cals_per_serving')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')
        servings = request.POST.get('servings')
        source = request.POST.get('source')

        # Build ingredients and instructions JSON
        details, ingredients, instructions = build_json_data(request)

        # validate details
        if details == "{}":
            pass
        elif not json.loads(details):
            valid = False

        # validate ingredients
        if not json.loads(ingredients):
            valid = False

        # validate instructions
        if not json.loads(instructions):
            valid = False

        # If all validation passes, Create Recipe
        if valid: 
            recipe = form.save(commit=False)

            if cals_per_serv:
                recipe.cals_per_serving = cals_per_serv

            if prep_time:
                recipe.prep_time = prep_time

            if cook_time:
                recipe.cook_time = cook_time

            if servings:
                recipe.servings = servings

            if source:
                recipe.source = source

            recipe.information = details
            recipe.ingredients = ingredients
            recipe.instructions = instructions
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
        'title': "New Recipe",
        'locked_details': {
            'servings': { 'name': 'Yield', 'value': '', 'type': 'text' },
            'cals_per_serving': { 'name': 'Calories Per Serving', 'value': '', 'type': 'number' },
            'prep_time': { 'name': "Prep Time", 'value': '', 'type': 'text' },
            'cook_time': { 'name': "Cook Time", 'value': '', 'type': 'text' },
            'source': { 'name': "Source", 'value': '', 'type': 'url'}
        },
        'sections': ['detail', 'ingredient', 'instruction'],
    }
    return render(request, 'recipes/recipe_edit.html', context)

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        
        # Validate Title and Description
        valid = True
        if not form.is_valid():
            valid = False
        
        cals_per_serv = request.POST.get('cals_per_serving')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')
        servings = request.POST.get('servings')
        source = request.POST.get('source')

        # Build ingredients and instructions JSON
        details, ingredients, instructions = build_json_data(request)

        # validate details
        if details == "{}":
            pass
        elif not json.loads(details):
            valid = False

        # validate ingredients
        if not json.loads(ingredients):
            valid = False
        
        # validate instructions
        if not json.loads(instructions):
            valid = False

        # If all validation passes, Update Recipe
        if valid: 
            recipe = form.save(commit=False)

            if cals_per_serv:
                recipe.cals_per_serving = cals_per_serv
            else:
                recipe.cals_per_serving = None

            if prep_time:
                recipe.prep_time = prep_time
            else:
                recipe.prep_time = None

            if cook_time:
                recipe.cook_time = cook_time
            else:
                 recipe.cook_time = None

            if servings:
                recipe.servings = servings
            else:
                recipe.servings = None

            if source:
                recipe.source = source
            else:
                recipe.source = None

            recipe.information = details
            recipe.ingredients = ingredients
            recipe.instructions = instructions
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)

    else:
        form = RecipeForm(instance=recipe)
    
    context = {
        'recipe': recipe,
        'form': form,
        'title': f'{ recipe.title } - Edit',
        'sections': ['detail', 'ingredient', 'instruction'],
        'locked_details': {
            'servings': { 'name': 'Yield', 'value': recipe.servings, 'type': 'text' },
            'cals_per_serving': { 'name': 'Calories Per Serving', 'value': recipe.cals_per_serving, 'type': 'number' },
            'prep_time': { 'name': "Prep Time", 'value': recipe.prep_time, 'type': 'text' },
            'cook_time': { 'name': "Cook Time", 'value': recipe.cook_time, 'type': 'text' },
            'source': { 'name': "Source", 'value': recipe.source, 'type': 'url'}
        },
        'details': json.loads(recipe.information),
        'ingredients': json.loads(recipe.ingredients),
        'instructions': json.loads(recipe.instructions),
        'detail_count': len(json.loads(recipe.information)),
        'ingredient_count': len(json.loads(recipe.ingredients)),
        'instruction_count': len(json.loads(recipe.instructions))

    }
    return render(request, 'recipes/recipe_edit.html', context)

# Edit/New Helper function
def build_json_data(request):
    # Build instructions and ingredients JSON
    details = {}
    detail_count = 0
    ingredients = {}
    ing_count = 0
    instructions = {}
    ins_count = 0

    for key, val in request.POST.items():
        if 'dynamic-field-detail' in key:
            details[str(detail_count)] = {'name': val.strip()}
            detail_index = key.split('-')[-1]
            details[str(detail_count)]['value'] = request.POST[f'dynamic-field-value-{ detail_index }']
            detail_count += 1
        elif 'dynamic-field-ingredient' in key:
            ingredients[str(ing_count)] = {'ingredient': val.strip()}
            ing_index = key.split('-')[-1]
            ingredients[str(ing_count)]['measurement'] = request.POST[f'dynamic-field-measurement-{ ing_index }']
            ing_count += 1
        elif 'dynamic-field-instruction' in key:
            instructions[str(ins_count)] = {'instruction': val.strip()}
            ins_count += 1
    if details == {}:
        details = str("{}")
    else:
        details = json.dumps(details)
    ingredients = json.dumps(ingredients)
    instructions = json.dumps(instructions)

    return details, ingredients, instructions

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
