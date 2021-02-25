from django.shortcuts import render


def main_page(request):
    return render(request, 'recipe_list.html')


def profile(request, **kwargs):
    return render(request, 'profile.html')


def recipe(request, **kwargs):
    return render(request, 'recipe_detail.html')
