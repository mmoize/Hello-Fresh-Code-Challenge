import os
from django.db import models
from django.db.models.signals import post_save
from authentication.models import User
from account.models import Profile
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy 
import datetime




class Tags(models.Model):
    name = models.CharField(max_length=20, blank=True, )

    def __str__(self):
        template = '{0.name}'
        return template.format(self)


class Allergen(models.Model):
    name = models.CharField(max_length=20, blank=True, )

    def __str__(self):
        template = '{0.name}'
        return template.format(self)



class Utensil(models.Model):
    name = models.CharField(max_length=20, blank=True, )

    def __str__(self):
        template = '{0.name}'
        return template.format(self)


class Ingredients(models.Model):
    Serving_Amount_For_Two = 2
    Serving_Amount_For_Four = 4

    Serving_Amount_Choices = (
        (Serving_Amount_For_Two, 2),
        (Serving_Amount_For_Four, 4)
    )

    # recipe = models.ManyToManyField(Recipe, related_name='recipes_ingredient', blank=True)
    name = models.CharField(max_length=300)
    photo = models.CharField(max_length=300)
    serving_amount = models.CharField(max_length=50, choices=Serving_Amount_Choices,default=2,blank=False)
    quantity = models.IntegerField()

    def __str__(self):
        template = '{0.name}'
        return template.format(self)


class Recipe(TimeStampedModel):
   
    Cooking_Difficulty_Easy = "Easy"
    Cooking_Difficulty_Medium = "Medium"
    Cooking_Difficulty_Hard = "Hard"

    Cooking_Difficulty_Choices = (
        (Cooking_Difficulty_Easy, "Easy"),
        (Cooking_Difficulty_Medium, "Medium"),
        (Cooking_Difficulty_Hard, "Hard")
    )

    name = models.CharField(max_length=150)
    photo = models.CharField(max_length=300)  #COuld've used ImageField, but this particular app isn't getting deployed.
    description = models.TextField()          #Describes the recipe
    prep_time = models.DurationField()        #Time takes to prepare the meal
    tags = models.ManyToManyField(Tags, related_name='tags', blank=True)
    cooking_difficulty = models.CharField(max_length=50, choices=Cooking_Difficulty_Choices,default="Medium",blank=False)
    allergens = models.ManyToManyField(Allergen, related_name='Allergens', blank=True)
    utensil = models.ManyToManyField(Utensil, related_name='Utensils', blank=True)
    ingredients = models.ManyToManyField(Ingredients,  blank=True)


    def no_of_ratings(self):
        ratings = Review.objects.filter(recipe=self)
        return len(ratings)
    def avg_rating(self):
        sum = 0
        ratings = Review.objects.filter(recipe=self)
        for rating in ratings:
            sum += rating.rate
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0


    def __str__(self):
        template = '{0.name}'
        return template.format(self)

    class Meta:
        ordering = ['-created',]



class Nutritionalvalue(models.Model):
    recipe =  models.OneToOneField(Recipe,  on_delete=models.CASCADE, blank=False)
    energy = models.IntegerField(blank=True, default=0)
    fat = models.DecimalField(blank=True, max_digits=7, decimal_places=1, default=0.0)
    of_which_saturates = models.DecimalField(max_digits=7, decimal_places=1, blank=True, default=0.0)
    Carbohydrate = models.DecimalField(max_digits=7, decimal_places=1, blank=True, default=0.0)
    of_which_sugars = models.DecimalField(max_digits=7, decimal_places=1, blank=True, default=0.0)
    dietary_fibre = models.IntegerField(blank=True, default=0)
    Protein = models.DecimalField(max_digits=7, decimal_places=1, blank=True, default=0.0)
    Cholesterol = models.IntegerField(blank=True, default=0)
    Sodium = models.IntegerField(blank=True, default=0)

    def __str__(self):
        template = '{0.name}'
        return template.format(self)



class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    description = models.TextField(blank=False) 
    step = models.IntegerField(blank=False, default=0)
    photo = models.CharField(blank=False, max_length=300)

class Review(TimeStampedModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(blank=True, max_length=300)
    rate = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
     
    class Meta:
        unique_together = (('user', 'Recipe'),)
        index_together =  (('user', 'Recipe'),)
    
    class Meta:
        ordering = ['-created',]



# Weekly Menu Class
class Weeklymenu(models.Model):
    #Picking the amount of poeple serving per week
    For_Two_People = 2
    For_Four_people = 4

    Number_Of_People_Choices = (
        (For_Two_People, 2),
        (For_Four_people, 4)
    )

    #Picking the amount of Recipes per week
    Three_Recipes = 3
    Four_Recipes = 4
    Five_Recipes = 5

    Amount_Of_Recipes_Choices = (
        (Three_Recipes, 3),
        (Four_Recipes, 4),
        (Five_Recipes, 5)
    )
    
    week_date = models.DateField(blank=False, default=datetime.now().strftime("%Y-%m-%d"))
    week_number = models.IntegerField(blank=False, default=0)
    number_ofpeople = models.CharField(max_length=50, choices=Number_Of_People_Choices,default=2,blank=False)
    weelkly_recipe_amount = models.CharField(max_length=50, choices=Amount_Of_Recipes_Choices,default=4,blank=False)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=ugettext_lazy('Users'))
    recipes = models.ManyToManyField(Recipe, related_name='weeklyrecipes', blank=True)



    def __str__(self):
        return self.customer.username



    
    

