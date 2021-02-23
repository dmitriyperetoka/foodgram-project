from django.shortcuts import render


def favourites(request, **kwargs):
    return render(request, 'favourites.html')


def subscriptions(request, **kwargs):
    return render(request, 'subscriptions.html')
