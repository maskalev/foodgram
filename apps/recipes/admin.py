from django.contrib import admin

from apps.recipes.models import (Ingredient, Tag, RecipeIngredients,
                                 Favorite, Purchase, Follow, Recipe)


class RecipeIngredientsInline(admin.TabularInline):
    """
    Inline class for RecipeIngredients model.
    """
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin class for Recipe model.
    """
    list_display = (
        'author',
        'title',
        'slug',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'author',
        'title',
        'tags',
    )
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        RecipeIngredientsInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin class for Tag model.
    """
    list_display = (
        'title',
        'slug',
        'color',
    )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'unit',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'title',
    )


admin.site.register(RecipeIngredients)
admin.site.register(Favorite)
admin.site.register(Purchase)
admin.site.register(Follow)
