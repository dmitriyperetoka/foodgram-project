from django.shortcuts import render


def purchase_list(request, **kwargs):
    return render(request, 'purchase_list.html')
