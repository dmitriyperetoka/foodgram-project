from django import forms

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class RecipeCreateForm(forms.ModelForm):
    """Prompt input date for creating recipes."""

    tags = forms.ModelMultipleChoiceField(
        Tag.objects.all(), to_field_name='slug')

    class Meta:
        model = Recipe
        fields = [
            'title', 'tags', 'cooking_time_minutes',
            'description', 'image']

    def __init__(self, data=None, **kwargs):
        if data is not None:
            data = data.copy()
            self.ingredients = self.get_ingredients(data)
            self.quantities = self.get_quantities(data)
        super().__init__(data=data, **kwargs)

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.save()

        ingredients_in_recipes = []
        for ingredient, quantity in zip(self.ingredients, self.quantities):
            ingredients_in_recipes.append(
                IngredientInRecipe(
                    recipe=recipe, ingredient=ingredient, quantity=quantity))

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
