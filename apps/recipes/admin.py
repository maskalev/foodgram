from django.contrib import admin

from apps.recipes.models import Ingredient, Recipe, Tag, RecipeIngredients


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
    prepopulated_fields = {'slug': ('title',)}
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
