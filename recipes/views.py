# recipes/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeForm

def index(request):
    recipes = Recipe.objects.order_by('-pk')[:5]
    return render(request, 'index.html', {'recipes': recipes, 'title': 'Home'})

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'title': 'Recipes'})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'title': recipe.title})

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
        'title': "New Recipe"
    }
    return render(request, 'recipes/recipe_edit.html', context)

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
        'title': f'{ recipe.title } - Edit'
    }
    return render(request, 'recipes/recipe_edit.html', context)

def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('recipe_list')

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
        
        return render(request, 'recipes/recipe_list.html', context)