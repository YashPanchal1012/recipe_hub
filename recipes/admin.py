from django.contrib import admin

from .models import Ingredient, Recipe


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "created_at"]  # Add fields you want to display and sort by


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
