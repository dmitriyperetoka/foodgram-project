from django.shortcuts import render


def subscriptions(request, **kwargs):
    return render(request, 'subscriptions.html')
