import json
import os
import sys, logging

import django
import requests
# Create your views here.
from django.contrib.postgres.aggregates import StringAgg
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, serializers, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK ,HTTP_201_CREATED
from rest_framework_simplejwt.state import User
from wordcloud import WordCloud

from .models import Recipe, Cusines
from .serializers import RecipeSerializer
from ..CaloriesPerDay.models import CaloriesPerDay
from ..Comments.models import Comments, CommentString
from ..Comments.serializers import CommentsSerializer
from ..Likes.models import Likes
from ..ingredient.models import Ingredient
from ..ingredient.views import customNutrientDecoder

from ..nutrient.models import Nutrient
import matplotlib.pyplot as plt
from django.core.files import File  # you need this somewhere
import urllib.request

from ..serializers import UserSerializer
from ..tag.models import Tag
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core import serializers as serializercore

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    user_id_param = openapi.Parameter('User ID', openapi.IN_QUERY, description="user id", type=openapi.TYPE_INTEGER)
    recipe_uuid_param = openapi.Parameter('Recipe UUID', openapi.IN_QUERY, description="Recipe Uuid", type=openapi.TYPE_STRING)
    comment_string_param = openapi.Parameter('Comment', openapi.IN_QUERY, description="Comment", type=openapi.TYPE_STRING)
    fdc_id_param = openapi.Parameter('FDC ID', openapi.IN_QUERY, description="Recipe Uuid", type=openapi.TYPE_STRING)
    search_param = openapi.Parameter('Search Query', openapi.IN_QUERY, description="Search Query", type=openapi.TYPE_STRING)
    recipe_response = openapi.Response('Recipe Serializer', RecipeSerializer)
    cuisine_response = openapi.Response('Portion Response', RecipeSerializer)

    def create(self, request, *args, **kwargs):
        # logger = logging.getLogger('django')
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(id=request.user.id)
            recipe = Recipe.objects.create(
                name=request.data['name'],
                preparation=request.data['preparation'],
                user=user,
                cuisine=request.data['cuisine'],
                calories=request.data['totalCalories'],
                difficulty=request.data['difficulty'],
                prep_time=request.data['prep_time'])
            nutrient_values ={}
            for ingredient in request.data['ingredients']:
                if (ingredient['fdcID'] != ''):
                    dummyIngredient = Ingredient.objects.create(name=ingredient['name'],
                                                                caloriesPerUnit=ingredient['energy'],
                                                                unitType="request.data['unitType']",  # todo
                                                                recipeUuid=request.data['name'],  # todo
                                                                fdcID=ingredient['fdcID'],
                                                                amount=ingredient['quantity']  # todo
                                                                )
                    dummyIngredient.save()
                    nutrients = ingredientQueryWithFdcNumber(ingredient['fdcID'])
                    for nutrient in nutrients.foodNutrients:
                        if len(nutrient) < 4:

                            dummy = Nutrient.objects.create(name=nutrient.nutrient.name,
                                                            unitName=nutrient.nutrient.unitName,
                                                            fdcNumber=nutrient.nutrient.number,
                                                            ingredientId=ingredient['fdcID'],
                                                            fdcId=nutrient[1].id,
                                                            amount=0)

                        else:
                            dummy = Nutrient.objects.create(name=nutrient.nutrient.name,
                                                            unitName=nutrient.nutrient.unitName,
                                                            fdcNumber=nutrient.nutrient.number,
                                                            ingredientId=ingredient['fdcID'],
                                                            fdcId=nutrient.id,
                                                            amount=nutrient.amount)
                            currentVal=nutrient_values.get(nutrient.nutrient.name)
                            if currentVal is None:
                                currentVal=0.0
                            currentVal+=nutrient.amount*(request.data['totalCalories']/ingredient['energy'])
                            nutrient_values.update({nutrient.nutrient.name:currentVal})
                        dummy.save()
                        dummyIngredient.nutrients.add(dummy)
                        dummyIngredient.save()
                    recipe.ingredients.add(dummyIngredient)
                    recipe.save()

            for tag in request.data['tags']:
                tag= Tag.objects.get_or_create(name=tag)
                tag[0].recipes.add(recipe)
                tag[0].save()
            nutrient_values.pop("Energy")
            wordcloud = WordCloud(background_color="white", width=500, height=500, max_words=len(nutrient_values), relative_scaling=0.5,
                           normalize_plurals=False).generate_from_frequencies(nutrient_values)

            # Display the generated image:
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(str(recipe.uuid)+'.png')
            recipe.recipe_image.save(os.path.basename(str(recipe.uuid)+'.png'),File(open(str(recipe.uuid)+'.png', 'rb')))
            recipe.save()
            os.remove(str(recipe.uuid)+'.png')
            print("recipe creation successfull")
            return Response(recipe.uuid, status=HTTP_201_CREATED)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='get', manual_parameters=[user_id_param], responses={200: recipe_response,400:'Recipe throws error'})
    @action(methods=["get"], url_path="getrecipes", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getrecipes(self, request, *args, **kwargs):
        try:
            recipes = Recipe.objects.filter(user=User.objects.get(id=request.query_params['id']))
            recipe_serializer = RecipeSerializer(recipes, many=True)
            return Response(recipe_serializer.data,HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='get', manual_parameters=[recipe_uuid_param], responses={200: recipe_response,400:'Recipe throws error'})
    @action(methods=["get"], url_path="getrecipe", detail=False, permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def getrecipe(self, request, *args, **kwargs):
        try:
            recipes = Recipe.objects.get(uuid=request.query_params['uuid'])
            recipe_serializer = RecipeSerializer(recipes, many=False)
            try:
                likes=Likes.objects.get(recipe=recipes)
                likesCount = likes.who_liked.count()
            except:
                likesCount=0
            try:
                comments=Comments.objects.filter(recipe=recipes)
                # allcomments = comments.get_all_comments()
                comment_serializer=CommentsSerializer(comments,many=True)
            except:
                for error in sys.exc_info():
                    print(str(error))
                allcomments=[]
            response={"recipe":recipe_serializer.data,
                      "likes":likesCount,
                      "comments":comment_serializer.data}
            return Response(response,HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='get', manual_parameters=[fdc_id_param,], responses={200: '"portions","image_url"',400:'Recipe throws error'})
    @action(methods=["get"], url_path="getportions", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getingredientPortions(self, request, *args, **kwargs):
        try:
            nutrients = ingredientQueryWithFdcNumber(request.query_params['fdcId'])
            url = 'https://commons.wikimedia.org/w/api.php'
            searchedIngredientName = str(request.query_params['searchNutrient']).lower()
            params = {
                "action": "query",
                "format": "json",
                "generator": "images",
                "prop": "imageinfo",
                "redirects": "l",
                "titles": searchedIngredientName,
                "iiprop": "timestamp|user|url"
            }
            image_url = requests.get(url=url, params=params)
            im_data = json.loads(image_url.text)
            if len(im_data) > 1:
                image_url = im_data['query']['pages'][next(iter(im_data['query']['pages']))]['imageinfo'][0]['url']
            else:
                image_url=""
            response_json = {"portions": nutrients.foodPortions,
                             "image_url": image_url}
            return Response(response_json,HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='get', manual_parameters=[], responses={200: cuisine_response,400:'Recipe throws error'})
    @action(methods=["get"], url_path="getcusines", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getcusines(self, request, *args, **kwargs):
        return Response(Cusines,HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[search_param], responses={200: recipe_response,400:'Recipe throws error'})
    @action(methods=["get"], url_path="search", detail=False, permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def search(self, request, *args, **kwargs):
        try:
            vector = SearchVector('name', weight='A') +SearchVector('cuisine', weight='B') +SearchVector(StringAgg('ingredients__name', delimiter=' '), weight='B')
            recipes = Recipe.objects.annotate(
                search=vector
            ).filter(search=request.query_params['query'])
            recipe_serializer = RecipeSerializer(recipes, many=True)
            return Response(recipe_serializer.data,HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='get', manual_parameters=[user_id_param,recipe_uuid_param], responses={200: 'OK',400:'Recipe throws error'})
    @action(methods=["get"], url_path="increaselike", detail=False, permission_classes=[permissions.IsAuthenticated])
    def increaselike(self, request, *args, **kwargs):
       try:
           # recipes = Recipe.objects.filter(user=User.objects.get(id=request.user.id))
           likes = Likes.objects.get_or_create(recipe=Recipe.objects.get(uuid=request.query_params['recipeid']))
           likes[0].who_liked.add(User.objects.get(id=request.query_params['userId']))
           return Response("ok", status=HTTP_200_OK)
       except:
           for error in sys.exc_info():
               print(str(error))
           return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(method='get', manual_parameters=[recipe_uuid_param,comment_string_param], responses={200: 'ok',400:'Recipe throws error'})
    @action(methods=["get"], url_path="writecomment", detail=False, permission_classes=[permissions.IsAuthenticated])
    def writecomment(self, request, *args, **kwargs):
        try:
            # recipes = Recipe.objects.filter(user=User.objects.get(id=request.user.id))
            user = User.objects.get(id=request.user.id)
            commentObject = Comments.objects.get_or_create(recipe=Recipe.objects.get(uuid=request.query_params['recipeid']),
                                                           commented_user=user)
            comment=CommentString.objects.create(comments_string=request.query_params['comment'])
            commentObject[0].comments.add(comment)
            return Response("ok", status=HTTP_201_CREATED)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='get', manual_parameters=[user_id_param], responses={200: recipe_response,400:'Recipe throws error'})
    @action(methods=["get"], url_path="getfollowingrecipes", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getfollowingrecipes(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.query_params['id'])
            followings = user.following.all()
            all_recipes=[]
            for following in followings:
                recipes = Recipe.objects.filter(user=User.objects.get(id=following.id))
                recipe_serializer = RecipeSerializer(recipes, many=True)
                all_recipes.append(recipe_serializer.data)
            return Response(all_recipes,HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(method='get', manual_parameters=[], responses={200: recipe_response,400:'Recipe throws error'})
    @action(methods=["get"], url_path="getallrecipes", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getallrecipes(self, request, *args, **kwargs):
        try:
            recipes = Recipe.objects.all()
            recipe_serializer = RecipeSerializer(recipes, many=True)
            return Response(recipe_serializer.data,HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Recipe throws error", status=HTTP_400_BAD_REQUEST)



def ingredientQueryWithFdcNumber(number):
    url = 'https://api.nal.usda.gov/fdc/v1/food/' + str(number) + '/'
    response = requests.get(url,
                            # params={'api_key': ''}
                            params={'api_key': ''}
                            )
    data = json.loads(response.text, object_hook=customNutrientDecoder)
    return data
