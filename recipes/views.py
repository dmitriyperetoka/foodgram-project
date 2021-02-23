from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def author_recipes(request, **kwargs):
    return render(request, 'author_recipes.html')


def recipe(request, **kwargs):
    return render(request, 'recipe.html')
