from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'dimension_unit']
    list_display_links = ['title']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_display_links = ['title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    list_display_links = ['title']


admin.site.register(IngredientInRecipe)
