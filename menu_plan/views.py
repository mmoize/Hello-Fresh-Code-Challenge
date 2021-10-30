from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from core.utils import MultipartJsonParser
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from datetime import date , datetime, timedelta
from authentication.models import User
from rest_framework.decorators import action
from .models import (
    Comments,
    Tags,
    Allergen,
    Utensil,
    Review,
    Comments,
    Recipe,
    Ingredients,
    Nutritionalvalue,
    Instruction,
    Weeklymenu,
)
from .serializers import (
    TagsSerializer,
    AllergensSerializer,
    UtensilsSerializer,
    IngredientsSerializer,
    NutritionalvaluesSerializer,
    InstructionsSerializer,
    RecipeSerializer,
    ReviewSerializer,
    WeeklymenuSerializer
)



# Recipe view for Creating a Recipe which is only done by a user with adming privileges
class RecipeView(ModelViewSet):
    permission_classes = (IsAuthenticated,)  
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    parser_classes = [MultipartJsonParser, JSONParser]
    lookup_field = "id"

    def get_serializer_context(self):
        context = super(RecipeView, self).get_serializer_context()
        # If images are included they could separeted here from the rest of the incoming information
        if len(self.request.data) > 0:
                context.update({
                'recipe_data': self.request.data
            })

        return context

    
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    def destroy(self,  request, *args, **kwargs):
        try:
            instance = self.get_object()
            id = instance.id
            self.perform_destroy(instance)
        except Exception:
            raise  NotFound(

                detail={
                    'message': 'Recipe was not found, provide an existing recipe id '
                }, code=406
            )

        responseData = {}   
        responseData = "The Recipe with ID "+ str(id)+ " was deleted."
        return Response(responseData, status=status.HTTP_204_NO_CONTENT)


    def get_queryset(self):

        return super().get_queryset()


    @action(detail=True)
    def get_one_recipe(self, pk, request, *args, **kwargs):

        
    
        serializer_context = {
            'request': request,
        }
        recipe = Recipe.objects.get(id=pk)
        serializer = RecipeSerializer(recipe, context=serializer_context)
        return Response(serializer.data)





#Review Recipe: Rate it and comment
class RateRecipeView(ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    serializer_class = RecipeSerializer
    parser_classes = [MultipartJsonParser, JSONParser]

    def update(self, request, id, *args, **kwargs):

        if 'rate' and 'comment' in request.data:
            recipe = Recipe.objects.get(id=id)
            user_rating = request.data['rate']
            user_comment = request.data['comment']
            currenlty_user = request.user

            try:
                review = Review.objects.get(user=currenlty_user.id, recipe=recipe.id)
                comment_obj = Comments.objects.create(user=currenlty_user, comment=user_comment)
                review.comments.add(comment_obj) 
                review.rate = user_rating
                review.save()
                serializer = ReviewSerializer(review, many=False)
                response = {'message': 'Review updated', 'result': serializer.data}
                return Response(response, status= status.HTTP_200_OK)
            except:
                comment_obj = Comments.objects.create(user=currenlty_user, comment=user_comment)
                review = Review.objects.create(
                    recipe = recipe,
                    user = currenlty_user,
                    rate = user_rating
                )

                review.comments.add(comment_obj)

                serializer = ReviewSerializer(review, many=False)
                response = {'message': 'Review was created', 'result': serializer.data}
                return Response(response, status= status.HTTP_200_OK)
 
        return super().update(request, *args, **kwargs)



# Recipe Update view
class RecipeUpdateView(UpdateAPIView):
    authentication_classes = (IsAuthenticated,)
    permission_classes = (IsAdminUser,)
    serializer_class = RecipeSerializer

    def get_object(self):
        recipe_id = self.kwargs['id']
        return Recipe.objects.get(id = recipe_id)
    
#Weelk
class UserWeeklyMenueView(ReadOnlyModelViewSet):
    queryset = Weeklymenu.objects.all()
    serializer_class = WeeklymenuSerializer


class WeeklyMenuView(ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    serializer_class = WeeklymenuSerializer
    queryset = Weeklymenu.objects.all()
    parser_classes = [MultipartJsonParser, JSONParser]
    lookup_field = "customer"

    def get_serializer_context(self):
        context = super(WeeklyMenuView, self).get_serializer_context()
        # If images are included they could separeted here from the rest of the incoming information
        if len(self.request.data) > 0:
                context.update({
                'Menu_Data': self.request.data
            })

        return context

    @action(detail=True)
    def get_user_one_week_menu(self, request, *args, **kwargs):
        Data = request.data
        serializer_context = {
            'request': request,
        }
        weeklymenu = Weeklymenu.objects.filter(customer=request.user.id, week_number=Data['week_number'])
        serializer = WeeklymenuSerializer(weeklymenu, context=serializer_context, many=True)

        return Response(serializer.data)

    @action(detail=True)
    def user_weekly_menu(self, request, *args, **kwargs):

        serializer_context = {
            'request': request,
        }
        weeklymenu = Weeklymenu.objects.filter(customer=request.user.id)
        serializer = WeeklymenuSerializer(weeklymenu, context=serializer_context, many=True)

        return Response(serializer.data)

    def get_queryset(self):
        weeklymenu = Weeklymenu.objects.filter(customer=self.request.user.id)
        return weeklymenu


    def update(self, request, *args, **kwargs):
        partial = True # Here I change partial to True
        Data = request.data
        weeklymenus = Weeklymenu.objects.filter(customer=self.request.user.id)

        if 'week_number' in Data:  # Update is for one specific menu
            weekmenu = Weeklymenu.objects.get(week_number=int(Data['week_number']))
            serializer = self.get_serializer(weekmenu, data=Data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
        else: # Update is for weekly Menus 
            for weekly_menu in weeklymenus:
                serializer = self.get_serializer(weekly_menu, data=Data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
        return Response(serializer.data)


    





        




 


  



   



