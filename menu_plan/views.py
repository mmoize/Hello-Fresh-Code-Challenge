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
from .models import (
    Tags,
    Allergen,
    Utensil,
    Review,
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
class RecipeCreateView(ModelViewSet):
    permission_classes = (IsAuthenticated,)  
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    parser_classes = [MultipartJsonParser, JSONParser]

    def get_serializer_context(self):
        context = super(RecipeCreateView, self).get_serializer_context()
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


class RecipeListView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = Recipe.objects.all()  
        return queryset


#Deleting Specific Recipe using and ID
class  DeleteRecipeView(APIView):
    permission_classes = (IsAuthenticated,) 

    def delete(self, request, id, format=None):

        try:
            Recipe.objects.filter(id=id).delete()
        except Exception:
            raise  NotFound(

                detail={
                    'message': 'Recipe was not found, provide an existing recipe id '
                }, code=406
            )

        responseData = {}   

        responseData = "The Recipe with ID "+ str(id)+ " was deleted." 

        return Response(responseData, status=status.HTTP_204_NO_CONTENT)


# Get A specific Recipe using ID or Name
class FindRecipeView(ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    serializer_class = RecipeSerializer
    parser_classes = [MultipartJsonParser, JSONParser]

    def get_queryset(self, *args, **kwargs):

        id = self.request.query_params.get('id')
       
        querySet= Recipe.objects.filter(id=id)
            
        return querySet

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
                review.comment = user_comment
                review.rate = user_rating
                review.save()
                serializer = ReviewSerializer(review, many=False)
                response = {'message': 'Review updated', 'result': serializer.data}
                return Response(response, status= status.HTTP_200_OK)
            except:
                review = Review.objects.create(
                    recipe = recipe,
                    user = currenlty_user,
                    comment = user_comment,
                    rate = user_rating
                )

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
    lookup_field = "id"

    def get_serializer_context(self):
        context = super(WeeklyMenuView, self).get_serializer_context()
        # If images are included they could separeted here from the rest of the incoming information
        if len(self.request.data) > 0:
                context.update({
                'Menu_Data': self.request.data
            })

        return context
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)

        return super().update(request, *args, **kwargs)





        




 


  



   



