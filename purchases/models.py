from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe as ProductSet

User = get_user_model()


class PurchaseList(models.Model):
    """Store purchase lists."""


class ProductSetInPurchaseList(models.Model):
    """Store the records of which quantity of certain product sets
    are included certain purchase lists.
    """
