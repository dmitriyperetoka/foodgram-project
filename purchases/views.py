from django.shortcuts import render


def new_purchase_list(request):
    return render(request, 'purchase_list.html')


def purchase_list(request, **kwargs):
    return render(request, 'purchase_list.html')
