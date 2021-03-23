from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class RecipeForm(forms.ModelForm):
    """Prompt input data for creating recipes."""

    tags = forms.ModelMultipleChoiceField(
        Tag.objects.all(), to_field_name='slug', label='Тэги',
        widget=forms.CheckboxSelectMultiple)
    cooking_time_minutes = forms.fields.IntegerField(
        min_value=1, widget=forms.NumberInput(
            attrs={'class': 'form__input', 'value': 1, 'autocomplete': 'off'}))

    class Meta:
        model = Recipe
        fields = [
            'title', 'tags', 'cooking_time_minutes', 'description', 'image'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form__input', 'autocomplete': 'off'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': 8}
            ),
            'image': forms.FileInput(attrs={'class': 'form__file'}),
        }

    def __init__(self, data=None, **kwargs):
        self.ingredientes = None

        if data is not None:
            titles = data.getlist('nameIngredient')
            quantities = data.getlist('valueIngredient')
            self.ingredientes = list(zip(titles, quantities))

        super().__init__(data=data, **kwargs)

    def clean(self):
        if not self.ingredientes:
            raise ValidationError('Не выбраны ингредиенты')

        unique_titles = set()
        for title, quantity in self.ingredientes:
            if title in unique_titles:
                raise ValidationError('Ингредиенты не должны повторяться')
            unique_titles.add(title)

        return super().clean()

    @transaction.atomic
    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.save()

        ingredients_in_recipes = []
        for title, quantity in self.ingredientes:
            ingredient = get_object_or_404(Ingredient, title=title)
            ingredients_in_recipes.append(
                IngredientInRecipe(
                    recipe=recipe, ingredient=ingredient, quantity=quantity))

        IngredientInRecipe.objects.filter(recipe=recipe).delete()
        IngredientInRecipe.objects.bulk_create(ingredients_in_recipes)
        self.save_m2m()
        return recipe
