from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Favourite(models.Model):
    """Store the records that certain recipes are in the favourite lists
    of certain users.
    """


class Ingredient(models.Model):
    """Store ingredients that can be included in recipes."""


class IngredientInRecipe(models.Model):
    """Store the records of which quantity of certain ingredients
    are included certain recipes.
    """


class Recipe(models.Model):
    """Store recipes."""


class Tag(models.Model):
    """Store tags that recipes can be filtered by."""
