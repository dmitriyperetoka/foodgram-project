from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class RecipeForm(forms.ModelForm):
    """Prompt input data for creating and editing recipes."""

    tags = forms.ModelMultipleChoiceField(
        Tag.objects.all(), to_field_name='slug', label='Тэги',
        widget=forms.CheckboxSelectMultiple)
    cooking_time_minutes = forms.fields.IntegerField(
        min_value=1, widget=forms.NumberInput(
            attrs={'class': 'form__input', 'value': 1, 'autocomplete': 'off'}))

    class Meta:
        model = Recipe
        fields = [
            'title', 'tags', 'cooking_time_minutes', 'description', 'image',
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form__input', 'autocomplete': 'off'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': 8}
            ),
            'image': forms.FileInput(
                attrs={'style': 'font-family: "Montserrat", sans-serif;'}
            ),
        }

    def __init__(self, data=None, **kwargs):
        self.ingredient_titles = None
        self.ingredient_quantities = None
        self.ingredients = None

        if data is not None:
            self.ingredient_titles = data.getlist('nameIngredient')
            self.ingredient_quantities = data.getlist('valueIngredient')

        super().__init__(data=data, **kwargs)

    def clean(self):
        if len(self.ingredient_titles) != len(self.ingredient_quantities):
            raise ValidationError(
                'У каждого ингредиента должны быть и название, и количество.')

        self.ingredients = list(
            zip(self.ingredient_titles, self.ingredient_quantities))
        if not self.ingredients:
            raise ValidationError('Нужно выбрать минимум один ингредиент.')

        all_ingredients = Ingredient.objects.all()
        unique_titles = set()
        for title, quantity in self.ingredients:
            if not (quantity.isdigit() and int(quantity) > 0):
                raise ValidationError(
                    'Количество ингредиента должно быть '
                    'целым положительным числом.')

            if title in unique_titles:
                raise ValidationError('Ингредиенты не должны повторяться.')
            unique_titles.add(title)

            if not all_ingredients.filter(title=title):
                raise ValidationError(
                    f'В базе данных нет ингредиента "{title}".')

        return super().clean()

    @transaction.atomic
    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.save()

        ingredients_in_recipes = []
        for title, quantity in self.ingredients:
            ingredient = get_object_or_404(Ingredient, title=title)
            ingredients_in_recipes.append(
                IngredientInRecipe(
                    recipe=recipe, ingredient=ingredient, quantity=quantity))

        IngredientInRecipe.objects.filter(recipe=recipe).delete()
        IngredientInRecipe.objects.bulk_create(ingredients_in_recipes)
        self.save_m2m()
        return recipe
