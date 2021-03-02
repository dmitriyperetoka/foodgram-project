from django.views.generic.base import TemplateView

from .models import NewPurchaseList


class NewPurchaseListView(TemplateView):
    template_name = 'purchase_list.html'

    def get_queryset(self):
        return NewPurchaseList.objects.get_or_create(
            author=self.request.user).prefetch_related('recipes')
