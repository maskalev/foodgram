from django.db import models


class Ingredient(models.Model):
    """
    Ingredient model.
    """
    name = models.CharField(max_length=255, verbose_name='Ingredient title',
                            unique=True)
    unit = models.CharField(max_length=30, verbose_name='Unit of measurement')

    def __str__(self):
        return f'{self.name} ({self.unit})'

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
