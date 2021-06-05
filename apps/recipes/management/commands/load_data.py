import csv

from django.core.management.base import BaseCommand, CommandError

from apps.recipes.models import Ingredient


class Command(BaseCommand):
    """
    Load ingredients from csv file.
    """
    def handle(self, *args, **options):
        try:
            with open('apps/recipes/data/ingredients.csv') as file:
                file_reader = csv.reader(file)
                for row in file_reader:
                    title, unit = row
                    Ingredient.objects.get_or_create(title=title, unit=unit)
        except Exception:
            raise CommandError('Ingredients was not upload!')
