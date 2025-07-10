from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_recipe, name="random"),
    path("advanced", views.advanced_search, name="advanced"),
    path("recipe/<int:recipe_id>", views.recipe, name="recipe"),
    path("load_recipe_cards", views.load_recipe_cards, name="load_recipe_cards"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
