from django.db import models

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    measurements = models.JSONField(blank=True, null=True)  # Store measurements as a JSON field
    instructions = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)  # Optional source of the recipe

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
