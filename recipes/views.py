import random

import requests
from django.http import JsonResponse
from django.shortcuts import render

from .models import Ingredient, Recipe


# Create your views here.
def fetch_from_api(api_url):
    response = requests.get(api_url)
    data = response.json() if response.status_code == 200 else {}
    return data.get("meals", [])


def index(request):
    if request.method == "GET":
        query = request.GET.get("query", "").strip().lower()
        if query:
            recipes = Recipe.objects.filter(title__icontains=query)
            return render(
                request,
                "recipes/index.html",
                {
                    "recipes": recipes,
                    "query": query,
                },
            )

    return render(
        request,
        "recipes/index.html",
    )


def random_recipe(request):
    recipe_id = random.randint(1, Recipe.objects.count())

    while not Recipe.objects.filter(id=recipe_id).exists():
        recipe_id = random.randint(1, Recipe.objects.count())

    return recipe(request, recipe_id)


def recipe(request, recipe_id):
    recipe_data = Recipe.objects.get(id=recipe_id)

    instructions = recipe_data.instructions.split("\n")
    ingredients = recipe_data.ingredients.all()
    measurements = recipe_data.measurements or {}
    ingredients = [
        {
            "name": ingredient.name,
            "measurement": measurements.get(ingredient.name, ""),
        }
        for ingredient in ingredients
    ]

    return render(
        request,
        "recipes/recipe.html",
        {
            "recipe": recipe_data,
            "instructions": instructions,
            "ingredients": ingredients,
        },
    )


def advanced_search(request):
    if request.method == "POST":
        selected_ingredients = request.POST.get("selected-ingredients").strip()

        selected_ingredients = [
            ingredient.strip()
            for ingredient in selected_ingredients.split(",")
            if ingredient
        ]

        all_recipes = Recipe.objects.all()
        recipes = []
        if selected_ingredients:
            for recipe in all_recipes:
                recipe_ingredients = [
                    ingredient.name for ingredient in recipe.ingredients.all()
                ]

                if all(
                    ingredient in recipe_ingredients
                    for ingredient in selected_ingredients
                ):
                    recipes.append(recipe)

        return render(request, "recipes/index.html", {"recipes": recipes})
    else:
        ingredients = [ingredient.name for ingredient in Ingredient.objects.all()]
        ingredients.sort()

        return render(
            request,
            "recipes/advanced.html",
            {
                "ingredients": ingredients,
            },
        )


def load_recipe_cards(request):
    recipes = []
    recipe_count = Recipe.objects.count()

    recipe_ids = []
    recipe_id = random.randint(1, recipe_count)

    for i in range(20):
        while recipe_id in recipe_ids:
            recipe_id = random.randint(1, recipe_count)
        recipe_ids.append(recipe_id)

    for id in recipe_ids:
        try:
            recipe = Recipe.objects.get(id=id)
            recipes.append(
                {
                    "id": recipe.id,  # type: ignore
                    "title": recipe.title,
                    "image_url": recipe.image_url,
                }
            )
        except Recipe.DoesNotExist:
            continue

    return JsonResponse({"recipes": recipes})
