from django import forms
from django.db import transaction

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class RecipeForm(forms.ModelForm):
    """Prompt input date for creating recipes."""

    tags = forms.ModelMultipleChoiceField(
        Tag.objects.all(), to_field_name='slug', label='Тэги',
        widget=forms.CheckboxSelectMultiple)
    cooking_time_minutes = forms.fields.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form__input'}), min_value=1)

    class Meta:
        model = Recipe
        fields = [
            'title', 'tags', 'cooking_time_minutes', 'description', 'image'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form__input'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': 8}
            ),
            'image': forms.FileInput(attrs={'class': 'form__file'}),
        }

    def __init__(self, data=None, **kwargs):
        if data is not None:
            data = data.copy()
            self.ingredients = self.get_ingredients(data)
            self.quantities = self.get_quantities(data)
        super().__init__(data=data, **kwargs)

    @transaction.atomic
    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.save()

        ingredients_in_recipes = []
        for ingredient, quantity in zip(self.ingredients, self.quantities):
            ingredients_in_recipes.append(
                IngredientInRecipe(
                    recipe=recipe, ingredient=ingredient, quantity=quantity))

        IngredientInRecipe.objects.filter(recipe=recipe).delete()
        IngredientInRecipe.objects.bulk_create(ingredients_in_recipes)
        self.save_m2m()
        return recipe

    @staticmethod
    def get_ingredients(data):
        ingredients = list()
        for key, value in data.items():
            if key.startswith('nameIngredient_'):
                ingredients.append(Ingredient.objects.get(title=value))

        return ingredients

    @staticmethod
    def get_quantities(data):
        quantities = list()
        for key, value in data.items():
            if key.startswith('valueIngredient_'):
                quantities.append(value)

        return quantities
