from uuid import uuid4

from django.core.exceptions import BadRequest
from django.db import IntegrityError, transaction
from django.forms import (CheckboxSelectMultiple, ModelForm, SelectMultiple,
                          Textarea)
from django.shortcuts import get_object_or_404
from pytils.translit import slugify

from apps.recipes.models import Ingredient, Recipe, RecipeIngredients


class TagForm(ModelForm):
    """
    Filter recipes by tags.
    """
    class Meta:
        model = Recipe
        fields = ('tags',)
        widgets = {
            'tags': SelectMultiple(),
        }


class RecipeForm(ModelForm):
    """
    Create, update and delete recipe.
    """
    def __init__(self, *args, **kwargs):
        self.ingredients = {}
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Validate recipeingredients data.
        """
        self.get_ingredients()
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, *args, **kwargs):
        """
        Save recipe.
        """
        user = kwargs.get('user')
        try:
            with transaction.atomic():
                recipe = super().save(commit=False)
                if recipe.author_id is None:
                    recipe.author = user
                slug = slugify(self.cleaned_data['title'])
                recipe.slug = slug
                recipe.save()
                recipe.recipeingredients.all().delete()
                ingredients = self.get_ingredients()
                ingredients_in_recipe = []
                for name, quantity in ingredients.items():
                    ingredients_in_recipe.append(RecipeIngredients(
                        recipe=recipe,
                        ingredient=get_object_or_404(
                            Ingredient, name__exact=name),
                        quantity=int(quantity),
                    ))
                RecipeIngredients.objects.bulk_create(ingredients_in_recipe)
                self.save_m2m()
        except IntegrityError as save_error:
            raise BadRequest('Error while saving') from save_error
        return recipe

    def get_ingredients(self):
        """
        Extract ingredients from recipe.
        """
        ingredients = {}
        for key, ingredient_name in self.data.items():
            if key.startswith('nameIngredient'):
                ingredient_value = self.data['valueIngredient' + key[14:]]
                ingredients[ingredient_name] = int(ingredient_value)
        return ingredients

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'tags', 'image', 'cooking_time',
                  'slug',)
        widgets = {
            'description': Textarea(attrs={'rows': 8}),
            'tags': CheckboxSelectMultiple(),
        }
