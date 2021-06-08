from django.contrib import admin

from apps.recipes.models import (Ingredient, Recipe, Tag, RecipeIngredients,
                                 Favorite, Purchase, Follow)


class RecipeIngredientsInline(admin.TabularInline):
    """
    Inline class for RecipeIngredients model.
    """
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    """
    Admin class for Recipe model.
    """
    prepopulated_fields = {'slug': ('title', 'author')}
    inlines = [
        RecipeIngredientsInline
    ]


class TagAdmin(admin.ModelAdmin):
    """
    Admin class for Tag model.
    """
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredients)
admin.site.register(Favorite)
admin.site.register(Purchase)
admin.site.register(Follow)
