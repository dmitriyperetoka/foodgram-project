from django.contrib import admin

from .models import (
    NewPurchaseList, PurchaseList, RecipeInNewPurchaseList,
    RecipeInPurchaseList,
)

admin.site.register(NewPurchaseList)
admin.site.register(PurchaseList)
admin.site.register(RecipeInNewPurchaseList)
admin.site.register(RecipeInPurchaseList)
