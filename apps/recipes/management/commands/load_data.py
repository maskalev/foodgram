import csv
import logging

from django.core.management.base import BaseCommand
from django.db import IntegrityError

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
        except IntegrityError:
            logging.error(msg='Ingredients are not unique.')
        except ValueError:
            logging.error(msg='Ingredients was not upload!')
