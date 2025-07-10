import requests
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Recipe


class Command(BaseCommand):
    help = "Fetch recipes from the TheMealDB API and save them to the database"

    def handle(self, *args, **kwargs):
        meals = []

        for i in range(26):
            api_url = (
                f"https://www.themealdb.com/api/json/v1/1/search.php?f={chr(97 + i)}"
            )
            response = requests.get(api_url)

            data = response.json() if response.status_code == 200 else {}

            if data.get("meals"):
                meals.extend(data["meals"])

        for meal in meals:
            # Build ingredients and measurements
            ingredients = []
            measurements = {}
            for i in range(1, 21):
                name = meal.get(f"strIngredient{i}")
                measurement = meal.get(f"strMeasure{i}")
                if name and name.strip():
                    ingredient, _ = Ingredient.objects.get_or_create(name=name.strip())
                    ingredients.append(ingredient)
                    measurements[name.strip()] = (
                        measurement.strip() if measurement else ""
                    )

            # Create or update the recipe
            recipe, _ = Recipe.objects.update_or_create(
                title=meal.get("strMeal"),
                defaults={
                    "instructions": meal.get("strInstructions", "").strip(),
                    "image_url": meal.get("strMealThumb"),
                    "measurements": measurements,
                    "source": meal.get("strSource", ""),
                },
            )
            # Set ingredients (ManyToMany)
            recipe.ingredients.set(ingredients)

            self.stdout.write("Recipe successfully created.")
