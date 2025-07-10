import re
from collections import defaultdict

import requests
from django.core.management.base import BaseCommand
from django.db.models import Q

from recipes.models import Ingredient, Recipe


class Command(BaseCommand):
    help = "Clean up the recipe data by removing invalid rows"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data cleanup...")
        self.remove_recipes_without_ingredients()
        self.remove_recipes_without_title()
        self.remove_recipes_without_instructions()
        self.remove_recipes_without_image_url()
        self.remove_ingredients_without_recipes()
        self.remove_invalid_ingredients()
        self.remove_duplicate_ingredients()
        self.reorder_recipes()
        self.stdout.write("Data cleanup completed.")

    def remove_recipes_without_ingredients(self):
        recipes_without_ingredients = Recipe.objects.filter(ingredients__isnull=True)
        count = recipes_without_ingredients.count()
        recipes_without_ingredients.delete()
        self.stdout.write(f"Deleted {count} recipes without ingredients.")

    def remove_recipes_without_title(self):
        recipes_without_title = Recipe.objects.filter(
            Q(title__isnull=True) | Q(title="")
        )
        count = recipes_without_title.count()
        recipes_without_title.delete()
        self.stdout.write(f"Deleted {count} recipes without a title.")

    def remove_recipes_without_instructions(self):
        recipes_without_instructions = Recipe.objects.filter(
            Q(instructions__isnull=True) | Q(instructions="")
        )
        count = recipes_without_instructions.count()
        recipes_without_instructions.delete()
        self.stdout.write(f"Deleted {count} recipes without instructions.")

    def remove_recipes_without_image_url(self):
        recipes_without_image_url = Recipe.objects.filter(
            Q(image_url__isnull=True) | Q(image_url="")
        )
        count = recipes_without_image_url.count()
        recipes_without_image_url.delete()
        self.stdout.write(f"Deleted {count} recipes without image URL.")

    def remove_ingredients_without_recipes(self):
        ingredients_without_recipes = Ingredient.objects.filter(recipes__isnull=True)
        count = ingredients_without_recipes.count()
        ingredients_without_recipes.delete()
        self.stdout.write(
            f"Deleted {count} ingredients not associated with any recipe."
        )

    def remove_invalid_ingredients(self):
        all_ingredients = Ingredient.objects.all()
        ingredients_with_invalid_names = []
        for ingredient in all_ingredients:
            if not ingredient.name or not ingredient.name.strip():
                ingredients_with_invalid_names.append(ingredient)
            elif len(ingredient.name) > 30:
                ingredients_with_invalid_names.append(ingredient)
        count = len(ingredients_with_invalid_names)
        for ingredient in ingredients_with_invalid_names:
            ingredient.delete()
        self.stdout.write(f"Deleted {count} invalid ingredients.")

    def remove_duplicate_ingredients(self):
        def normalize_name(name):
            return re.sub(r"[^a-zA-Z ]", "", name or "").strip().lower()

        all_ingredients = Ingredient.objects.all()
        ingredient_map = defaultdict(list)
        for ingredient in all_ingredients:
            norm_name = normalize_name(ingredient.name)
            if norm_name:
                ingredient_map[norm_name].append(ingredient)

        for norm_name, ingredients in ingredient_map.items():
            if not norm_name or not norm_name.replace(" ", "").isalpha():
                for ingredient in ingredients:
                    ingredient.delete()
                continue
            first_ingredient = ingredients[0]
            for duplicate in ingredients[1:]:
                for recipe in duplicate.recipes.all():
                    recipe.ingredients.add(first_ingredient)
                    if (
                        recipe.measurements
                        and duplicate.name != first_ingredient.name
                        and duplicate.name in recipe.measurements
                    ):
                        recipe.measurements[first_ingredient.name] = (
                            recipe.measurements[duplicate.name]
                        )
                        del recipe.measurements[duplicate.name]
                        recipe.save()
                    recipe.ingredients.remove(duplicate)
                duplicate.delete()
            first_ingredient.name = norm_name.title()
            first_ingredient.save()
        self.stdout.write("Ingredient cleanup completed.")

    def reorder_recipes(self):
        recipes = Recipe.objects.all()
        for i, recipe in enumerate(recipes, start=1):
            recipe.id = i  # type: ignore
            recipe.save()
        self.stdout.write("Reordered recipes by ID.")
