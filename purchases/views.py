from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from .models import NewPurchaseList


@method_decorator(login_required, 'dispatch')
class NewPurchaseListView(TemplateView):
    template_name = 'purchase_list.html'

    def get_queryset(self):
        return NewPurchaseList.objects.get_or_create(
            author=self.request.user).prefetch_related('recipes')
