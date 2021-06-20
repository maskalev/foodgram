from uuid import uuid4

from django.core.exceptions import BadRequest, ValidationError
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

    def create_recipe_ingredients(self, recipe):
        """
        Add ingredients to the new recipe.
        """
        ingredients_to_create = []
        for ingredient_title, quantity in self.ingredients.items():
            ingredient = get_object_or_404(Ingredient,
                                           title=ingredient_title)
            recipeingredients = RecipeIngredients(recipe=recipe,
                                                  ingredient=ingredient,
                                                  quantity=quantity)
            ingredients_to_create.append(recipeingredients)
        RecipeIngredients.objects.bulk_create(ingredients_to_create)

    def clean(self):
        """
        Validate recipeingredients data.
        """
        self.get_ingredients()
        cleaned_data = super().clean()
        if not self.ingredients:
            error_message = ValidationError('Ingredients list is empty')
            self.add_error(None, error_message)
        for value in self.ingredients.values():
            if value <= 0:
                error_message = ValidationError('Quantity must be positive')
                self.add_error(None, error_message)
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
                if Recipe.objects.filter(slug=slug).exists():
                    slug = uuid4()
                recipe.slug = slug
                recipe.save()
                self.create_recipe_ingredients(recipe)
                self.save_m2m()
        except IntegrityError as save_error:
            raise BadRequest('Error while saving') from save_error
        return recipe

    def get_ingredients(self):
        """
        Extract ingredients from recipe.
        """
        for key, ingredient_name in self.data.items():
            if key.startswith('nameIngredient'):
                ingredient_value = self.data['valueIngredient' + key[14:]]
                try:
                    self.ingredients[ingredient_name] = float(ingredient_value)
                except ValueError:
                    self.ingredients[ingredient_name] = None

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'tags', 'image', 'cooking_time',
                  'slug',)
        widgets = {
            'description': Textarea(attrs={'rows': 8}),
            'tags': CheckboxSelectMultiple(),
        }
