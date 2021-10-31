from rest_framework import serializers
from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework.exceptions import NotAcceptable
from datetime import date, timedelta
import datetime
import random
import ast
import inspect
from .models import (
    Tags,
    Allergen,
    Utensil,
    Recipe,
    Ingredients,
    Nutritionalvalue,
    Instruction,
    Review,
    Comments,
    Weeklymenu
)


class TagsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:tags-detail", read_only=True, lookup_field="tags")

    class Meta:
        model = Tags
        fields = ['url', 'name', 'id']


class AllergensSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:allergen-detail", read_only=True, lookup_field="allergen")

    class Meta:
        model = Allergen
        fields = ['url', 'name', 'id']


class UtensilsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:utensil-detail", read_only=True, lookup_field="utensil")

    class Meta:
        model = Utensil
        fields = ['url', 'name', 'id']


class IngredientsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:ingredients-detail", read_only=True, lookup_field="ingredients")

    class Meta:
        model = Ingredients
        fields = ['id', 'url', 'name', 'photo', 'quantity', 'serving_amount']


class NutritionalvaluesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:nutritionalvalue-detail", read_only=True, lookup_field="nutritionalvalue")
    recipe = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:recipe-detail", read_only=True, source="recipe_name")

    class Meta:
        model = Nutritionalvalue
        fields = [
            'id', 'url', 'recipe',
            'energy', 'fat', 'of_which_saturates',
            'Carbohydrate', 'of_which_sugars',
            'dietary_fibre', 'Protein', 'Cholesterol', 'Sodium']


class InstructionsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:instruction-detail", read_only=True, lookup_field="instruction")
    recipe = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:recipe-detail", read_only=True, source="recipe_name")

    class Meta:
        model = Instruction
        fields = ['id', 'url', 'description', 'photo', 'step', 'recipe']


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagsSerializer(allow_null=True, many=True, read_only=True)
    allergens = AllergensSerializer(allow_null=True, many=True, read_only=True)
    utensil = UtensilsSerializer(allow_null=True, many=True, read_only=True, )
    ingredients = IngredientsSerializer(
        allow_null=True, read_only=True, many=True, )
    nutritionalvalue = NutritionalvaluesSerializer(
        allow_null=True, read_only=True,)
    instruction_set = InstructionsSerializer(
        allow_null=True, read_only=True, many=True)
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:recipe-detail", read_only=True, lookup_field="pk")

    class Meta:
        model = Recipe
        fields = [
            "url", "id", "name",
            'photo', "description",
            "prep_time", 'cooking_difficulty',
            "tags", "allergens", "utensil",
            "ingredients", "nutritionalvalue",
            "instruction_set", 'no_of_ratings', 'avg_rating'
        ]

    def create(self, validated_data):

        Data = self.context['recipe_data']

        Recipe_name = validated_data['name']
        Recipe_photo = validated_data['photo']
        Recipe_description = validated_data['description']
        Recipe_preptime = validated_data['prep_time']
        Recipe_cookingdifficulty = validated_data['cooking_difficulty']

        Recipe_Obj = Recipe.objects.create(
            name=Recipe_name.lower(),
            photo=Recipe_photo.lower(),
            description=Recipe_description.lower(),
            prep_time=Recipe_preptime,
            cooking_difficulty=Recipe_cookingdifficulty
        )

        if 'tags' in Data:
            tags_list = Data['tags']
            TagsData = tags_list.split(',')
            for Tag_data in TagsData:
                Tags_Obj, created = Tags.objects.get_or_create(name=Tag_data)
                Recipe_Obj.tags.add(Tags_Obj)

        if 'allergen' in Data:
            allergen_list = Data['allergen']
            AllergensData = allergen_list.split(',')
            for allergen_data in AllergensData:
                Allergen_Obj, created = Allergen.objects.get_or_create(
                    name=allergen_data)
                Recipe_Obj.allergens.add(Allergen_Obj)

        if 'utensil' in Data:
            utensil_list = Data['utensil']
            UtensilsData = utensil_list.split(",")
            for Utensil_data in UtensilsData:
                Utensils_Obj, created = Utensil.objects.get_or_create(
                    name=Utensil_data)
                Recipe_Obj.utensil.add(Utensils_Obj)

        if 'nutritionalvalues' in Data:
            NutritionalValuesData = ast.literal_eval(
                str(Data['nutritionalvalues']))
            Nutritionalvalue.objects.get_or_create(
                recipe=Recipe_Obj,
                energy=NutritionalValuesData['energy'],
                fat=NutritionalValuesData['fat'],
                of_which_saturates=NutritionalValuesData['of_which_saturates'],
                Carbohydrate=NutritionalValuesData['carbohydrate'],
                of_which_sugars=NutritionalValuesData['of_which_sugars'],
                dietary_fibre=NutritionalValuesData['dietary_fibre'],
                Protein=NutritionalValuesData['Protein'],
                Cholesterol=NutritionalValuesData['Cholesterol'],
                Sodium=NutritionalValuesData['sodium']
            )

        if 'ingredients' in Data:
            IngredientsData = ast.literal_eval(
                inspect.cleandoc(Data['ingredients']))
            for i in IngredientsData:
                Ingredient_Obj = Ingredients.objects.get_or_create(
                    name=i['name'],
                    photo=i['photo'],
                    serving_amount=int(i['serving_amount']),
                    quantity=int(i['quantity'])
                )
                Ingre_data = Ingredient_Obj[0]
                Recipe_Obj.ingredients.add(Ingre_data.id)

        if 'instructions' in Data:
            InstructionsData = ast.literal_eval(
                inspect.cleandoc(Data['instructions']))

            for i in InstructionsData:
                Instruction.objects.get_or_create(
                    recipe=Recipe_Obj,
                    description=i['description'],
                    step=int(i['step']),
                    photo=i['photo']
                )

        return Recipe_Obj

    def update(self, instance, validated_data):

        if 'name' in validated_data:
            instance.name = validated_data.pop('name')
        if 'photo' in validated_data:
            instance.photo = validated_data.pop('photo')
        if 'description' in validated_data:
            instance.description = validated_data.pop('description')
        if 'prep_time' in validated_data:
            instance.prep_time = validated_data.pop('prep_time')
        if 'cooking_difficulty' in validated_data:
            instance.cooking_difficulty = validated_data["cooking_difficulty"]

        instance.save()
        return instance


class CommentsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:review-detail", read_only=True, lookup_field="review")
    user = UserSerializer(read_only=True,)

    class Meta:
        model = Comments
        fields = ['url', 'id', 'user', 'comment']


class ReviewSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:review-detail", read_only=True, lookup_field="review")
    comments = CommentsSerializer(allow_null=True, many=True, read_only=True)
    user = UserSerializer(read_only=True,)

    class Meta:
        model = Review
        fields = ['url', 'id', 'rate', 'user', 'comments', 'recipe']


class WeeklymenuSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="menu_plan:weeklymenu-detail", read_only=True, lookup_field="customer")
    recipes = RecipeSerializer(allow_null=True, read_only=True, many=True, )
    customer = UserSerializer(read_only=True,)

    class Meta:
        model = Weeklymenu
        fields = ['url', 'id', 'week_date', 'week_number',
                  'number_ofpeople', 'weelkly_recipe_amount', 'customer', 'recipes']
        lookup_field = "customer"
        lookup_value_regex = "[^/]+"

    def create(self, validated_data):
        # Customer needs 52 weeks of weely menu recipes.
        # Code below calculates the Dates from the time of weelky menu created
        Weeklymenu_Obj = Weeklymenu.objects.filter(
            customer=self.context['request'].user)

        if Weeklymenu_Obj.exists():
            raise NotAcceptable(
                detail={
                    'message': "The request is not acceptable. Weekly Menu's already created "
                }, code=406)

        else:
            today = datetime.date.today()
            i = 1
            week_count = 53       # Adding 53 weeks, due to the fact that python will start at 0
            for week in range(week_count):
                if week == 0:  # Don't mind the zero here
                    pass
                else:
                    # Code below calculates the date from today.
                    coming_weeks_date = today + datetime.timedelta(days=week*7)
                    # Creating Weekly menu object
                    Weeklymenu_Obj = Weeklymenu.objects.create(
                        week_date=coming_weeks_date,
                        week_number=i,
                        number_ofpeople=validated_data['number_ofpeople'],
                        weelkly_recipe_amount=validated_data['weelkly_recipe_amount'],
                        customer=self.context['request'].user
                    )
                    # Creat a list of all available recipes
                    RecipesList = list(Recipe.objects.all())

                    weekly_Amount_ofRecipes = validated_data['weelkly_recipe_amount']
                    # Populates the many to many recipe field in WeeklyMenu model
                    # It basically assigns the customer recipes
                    if weekly_Amount_ofRecipes == 3:
                        random_Recipe = random.sample(RecipesList, 3)
                        for recipe in random_Recipe:
                            Weeklymenu_Obj.recipes.add(recipe)

                    elif weekly_Amount_ofRecipes == 4:
                        random_Recipe = random.sample(RecipesList, 4)
                        for recipe in random_Recipe:
                            Weeklymenu_Obj.recipes.add(recipe)

                    elif weekly_Amount_ofRecipes == 5:
                        random_Recipe = random.sample(RecipesList, 5)
                        for recipe in random_Recipe:
                            Weeklymenu_Obj.recipes.add(recipe)
                    i += 1

        return Weeklymenu_Obj

    # Custom Update for selecting Recipe
    def update(self, instance, validated_data):

        # For accessing none validated Data
        Data = self.context['Menu_Data']

        RecipesList = list(Recipe.objects.all())

        if 'week_number' not in Data:  # Update  all weekly menus
            # Searching the DB for all recipes with the Ingredients Quantiy based on the number
            # - number of people to be served, thus passing the validated Data.
            if 'number_ofpeople' in validated_data:
                instance.number_ofpeople = validated_data['number_ofpeople']

                try:
                    RecipesList = list(Recipe.objects.filter(
                        ingredients__serving_amount=validated_data['number_ofpeople']))

                except Exception:
                    raise NotAcceptable(
                        detail={
                            'message': 'The request is not acceptable. Current number of Recepes is  < 3, Admin needs to add more recipes.'
                        }, code=406)

            # Selecting number of recipes for this particular week
            # -if the customer provides an option from the  choices 3, 4 or 5 meals a weak.
            if 'weelkly_recipe_amount' in validated_data:
                instance.weelkly_recipe_amount = validated_data['weelkly_recipe_amount']
                weekly_Amount_ofRecipes = validated_data['weelkly_recipe_amount']

                if weekly_Amount_ofRecipes == 3:
                    random_Recipe = random.sample(RecipesList, 3)
                    for recipe in random_Recipe:
                        instance.recipes.add(recipe)

                elif weekly_Amount_ofRecipes == 4:
                    random_Recipe = random.sample(RecipesList, 4)
                    for recipe in random_Recipe:
                        instance.recipes.add(recipe)

                elif weekly_Amount_ofRecipes == 5:
                    random_Recipe = random.sample(RecipesList, 5)
                    for recipe in random_Recipe:
                        instance.recipes.add(recipe)

        else:  # Update for one specific week menu.

            # Customer may choose to change auto-assigned recipes
            if 'change_recipe' in Data:

                Change_Recipe_StrList = Data['change_recipe']
                # splitting String "ID, ID" to a list [ID,ID]
                Change_Recipe_IDS = Change_Recipe_StrList.split(',')

                # Old recipe ID is the first element in the splitted string
                Existing_Recipe_ID = Change_Recipe_IDS[0]
                Old_Recipe_Obj = Recipe.objects.get(id=Existing_Recipe_ID)
                # New recipe ID is the second element in the splitted string
                New_Recipe_ID = Change_Recipe_IDS[1]
                New_Recipe_Obj = Recipe.objects.get(id=New_Recipe_ID)

                # Deleting the old recipe from this particular week's menu
                instance.recipes.remove(Old_Recipe_Obj)
                # Add new recipe
                instance.recipes.add(New_Recipe_Obj)

        instance.save()
        return instance
