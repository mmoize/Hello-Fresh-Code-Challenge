from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework import renderers

from menu_plan.models import Weeklymenu
from .views import (
    RecipeView,
    RateRecipeView,
    RecipeUpdateView,
    WeeklyMenuView
)

app_name = 'menu_plan'




recipe_review = RateRecipeView.as_view({'put': 'update',})

recipe_detail = RecipeView.as_view({
    'get': 'list',
    'put': 'create',
    'patch': 'update',
    'delete': 'destroy',
    'post':'create'
})
recipe_createview = RecipeView.as_view({'post': 'create'})
get_recipe_detail = RecipeView.as_view({'get': 'retrieve'})



weeklymenu_list = WeeklyMenuView.as_view({
    'get': 'list',
    'post': 'create'
})
weeklymenu_detail = WeeklyMenuView.as_view({
    'get': 'retrieve',
    'put': 'create',
    'patch': 'update',
    'delete': 'destroy'
})
weeklymenu_user_weekly_menu = WeeklyMenuView.as_view({
    'get': 'user_weekly_menu'
})
get_user_one_week_menu = WeeklyMenuView.as_view({
    'get': 'get_user_one_week_menu'
})


urlpatterns = [
    # Recipes
    path('recipe/<int:id>/',recipe_detail,name='recipe_detail'),
    path('recipe/<int:id>',get_recipe_detail,name='get_recipe_detail'),
    path('recipe/',recipe_detail,name='recipe_detail'),
    path('recipe_create/',recipe_createview,name='recipe_createview'),
    path('recipereview/<int:id>/', recipe_review,name='recipe_review'),

    #Weekly Menu
    path('weeklymenu/<int:customer>/', weeklymenu_detail,name='weeklymenu_detail'),
    path('weeklymenu/<int:customer>/user/', weeklymenu_user_weekly_menu, name='weeklymenu_user_weekly_menu'),
    path('weeklymenu/<int:customer>/week/', get_user_one_week_menu, name='get_user_one_week_menu')
    
]


