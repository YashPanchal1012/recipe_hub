import requests
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Recipe

ID_START = 1200
ID_END = 1400

class Command(BaseCommand):
    help = "Fetch recipes from the SpoonacularAPI and save them to the database"

    def handle(self, *args, **kwargs):        
        meals = []
        ids = ",".join(str(i) for i in range(ID_START, ID_END))

        api_key = "4a32000b81e6429198f51e1e446b3b09"

        api_url = f"https://api.spoonacular.com/recipes/informationBulk?apiKey={api_key}&ids={ids}"
        response = requests.get(api_url)

        data = response.json() if response.status_code == 200 else []

        meals.extend(data)

        for meal in meals:
            # Build ingredients and measurements
            extended_ingredients = meal.get("extendedIngredients", [])
            ingredients = []
            measurements = {}

            if extended_ingredients:
                for ingredient in extended_ingredients:
                    name = ingredient.get("name")
                    measurement_path = ingredient.get("measures").get("us")
                    measurement = (
                        f"{measurement_path.get('amount')} {measurement_path.get('unitShort')}"
                    )

                    if name and name.strip():
                        ingredient, _ = Ingredient.objects.get_or_create(
                            name=name.strip()
                        )
                        ingredients.append(ingredient)
                        measurements[name.strip()] = (
                            measurement.strip() if measurement else ""
                        )

            analyzed_instructions = meal.get("analyzedInstructions", [])
            instructions = []

            if analyzed_instructions:
                for step in analyzed_instructions[0].get("steps"):
                    instructions.append(step.get("step", ""))

            # Create or update the recipe
            recipe, _ = Recipe.objects.update_or_create(
                title=meal.get("title"),
                defaults={
                    "instructions": "\n".join(instructions),
                    "image_url": meal.get("image"),
                    "measurements": measurements,
                    "source": meal.get("sourceUrl", ""),
                },
            )
            # Set ingredients (ManyToMany)
            recipe.ingredients.set(ingredients)

            self.stdout.write("Recipe successfully created.")
