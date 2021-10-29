from django.urls import path
from rest_framework.routers import DefaultRouter

from menu_plan.models import Weeklymenu
from .views import (
    RecipeCreateView,
    RecipeListView,
    DeleteRecipeView,
    FindRecipeView,
    RateRecipeView,
    RecipeUpdateView,
    WeeklyMenuView
)

app_name = 'menu_plan'

recipe_createview = RecipeCreateView.as_view({'post': 'create'})
recipe_viewlist = RecipeListView.as_view({'get': 'list'})
recipe_findview = FindRecipeView.as_view({'get': 'list'})
recipe_review = RateRecipeView.as_view({'put': 'update',})

weeklymenu_list = WeeklyMenuView.as_view({
    'get': 'list',
    'post': 'create'
})

weeklymenu_detail = WeeklyMenuView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})



urlpatterns = [
    # Recipes
    path('create_recipe/',recipe_createview,name='recipe_create'),
    path('recipelist/',recipe_viewlist,name='recipe_list'),
    path('recipefind/', recipe_findview,name='recipe_find'),
    path('recipereview/<int:id>/', recipe_review,name='recipe_review'),
    path('recipe/delete/<int:id>/', DeleteRecipeView.as_view(), name='receipe_delete'),

    #Weekly Menu
    path('weeklymenu/<int:id>/', weeklymenu_detail,name='weeklymenu_detail'),
    
    
]


