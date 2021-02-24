from django.shortcuts import render


def main_page(request):
    return render(request, 'main_page.html')


def profile(request, **kwargs):
    return render(request, 'profile.html')


def recipe(request, **kwargs):
    return render(request, 'recipe.html')
