import pytest
from model_bakery import baker

from menu_plan.models import Ingredients



def urbb():
    def unfilled_recipe_bakery_batch(n):
        urbb = baker.make(
            'recipe.Recipe',
            _fill_optional = [
                'name',
                'photo',
                'description',
                'prep_time',
                'tags',
                'cooking_difficulty',
                'allergens',
                'utensil',
                'ingredients'
            ],
            _quantity=n
        )
        return urbb
    return unfilled_recipe_bakery_batch


@pytest.fixture
def frbb():
    def filled_recipe_bakery_batch(n):
        urbb = baker.make(
            'recipe.Recipe',
            _quantity=n,
        )
        return urbb
    return filled_recipe_bakery_batch

@pytest.fixture
def frb():
    def filled_recipe_bakery():
        urbb = baker.make(
            'recipe.Recipe',
            tags = baker.make('recipe.Tags'),
            ingredients = baker.make('recipe.Ingredients'),
            allergens = baker.make('recipe.Allergen'),
            utensil = baker.make('recipe.Utensil'),
        )
        return urbb
    return filled_recipe_bakery


