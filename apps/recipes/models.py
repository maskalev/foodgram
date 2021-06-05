from django.core.validators import MinValueValidator
from django.db import models

from apps.users.models import User


class Ingredient(models.Model):
    """
    Ingredient model.
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Ingredient title',
        unique=True
    )
    unit = models.CharField(
        max_length=30,
        verbose_name='Unit of measurement'
    )

    def __str__(self):
        return f'{self.name} ({self.unit})'

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class Tag(models.Model):
    """
    Tag model (breakfast, lunch and dinner).
    """
    title = models.CharField(
        max_length=20,
        verbose_name='Tag title'
    )
    slug = models.SlugField(
        max_length=20,
        db_index=True,
        unique=True,
        verbose_name='Tag slug',
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Recipe(models.Model):
    """
    Recipe model.
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Title',
    )
    description = models.TextField(
        verbose_name='Description',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Тэги',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Image',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time, min',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredients',
        verbose_name='Ingredients',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication date',
    )
    slug = models.SlugField(
        max_length=250,
        db_index=True,
        unique=True,
        verbose_name='Recipe slug',
    )

    def __str__(self):
        return f'{self.title}, {self.author}, {self.pub_date}'

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


class RecipeIngredients(models.Model):
    """
    Link between recipes and ingredients.
    """
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ingredient',
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=(MinValueValidator(0),),
        verbose_name='Quantity',
    )

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}, {self.quantity}'

    class Meta:
        verbose_name_plural = 'RecipesIngredients'
        verbose_name = 'RecipeIngredients'
        constraints = [
            models.UniqueConstraint(fields=('recipe', 'ingredient'),
                                    name='unique_link'),
        ]
