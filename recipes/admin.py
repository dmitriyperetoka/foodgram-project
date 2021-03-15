from django.contrib import admin
from django.db import models

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'dimension_unit']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_display_links = ['title']
    list_filter = ['author', 'title', 'tags']
    readonly_fields = ['favorite_lists_count']
    search_fields = ['title', 'description']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            favorite_lists_count=models.Count('favorite_lists'))

    def favorite_lists_count(self, obj):
        return obj.favorite_lists_count

    favorite_lists_count.short_description = (
        'Количество добавлений в список избранного')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    list_display_links = ['title']
    search_fields = ['title']


admin.site.register(IngredientInRecipe)
