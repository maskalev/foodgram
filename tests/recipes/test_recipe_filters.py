from django.test import TestCase

from apps.recipes.templatetags.recipe_filters import remainsrecipesnumber


class RecipeFiltersTest(TestCase):
    def test_remainsrecipesnumber(self):
        """
        Function return the correct phrase.
        """
        test_data = {
            4: "Ещё 1 рецепт...",
            5: "Ещё 2 рецепта...",
            6: "Ещё 3 рецепта...",
            7: "Ещё 4 рецепта...",
            8: "Ещё 5 рецептов...",
            9: "Ещё 6 рецептов...",
            10: "Ещё 7 рецептов...",
            11: "Ещё 8 рецептов...",
            12: "Ещё 9 рецептов...",
            13: "Ещё 10 рецептов...",
            14: "Ещё 11 рецептов...",
            15: "Ещё 12 рецептов...",
            16: "Ещё 13 рецептов...",
            17: "Ещё 14 рецептов...",
            18: "Ещё 15 рецептов...",
            19: "Ещё 16 рецептов...",
            20: "Ещё 17 рецептов...",
            21: "Ещё 18 рецептов...",
            22: "Ещё 19 рецептов...",
            23: "Ещё 20 рецептов...",
            24: "Ещё 21 рецепт...",
            25: "Ещё 22 рецепта...",
            26: "Ещё 23 рецепта...",
            27: "Ещё 24 рецепта...",
            28: "Ещё 25 рецептов...",
            29: "Ещё 26 рецептов...",
            30: "Ещё 27 рецептов...",
            31: "Ещё 28 рецептов...",
            32: "Ещё 29 рецептов...",
            33: "Ещё 30 рецептов...",
            34: "Ещё 31 рецепт...",
        }
        for number, phrase in test_data.items():
            assert remainsrecipesnumber(number) == phrase
