from django.db import models


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
        max_length=255,
        verbose_name='Tag title'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
