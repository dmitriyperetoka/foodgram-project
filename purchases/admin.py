from django.contrib import admin

from .models import ProductSetInPurchaseList, PurchaseList


class ProductSetInPurchaseListAdmin(admin.ModelAdmin):
    pass


class PurchaseListAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProductSetInPurchaseList, ProductSetInPurchaseListAdmin)
admin.site.register(PurchaseList, PurchaseListAdmin)
