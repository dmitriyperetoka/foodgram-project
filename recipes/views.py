from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def profile(request, **kwargs):
    return render(request, 'profile.html')


def recipe(request, **kwargs):
    return render(request, 'recipe.html')
