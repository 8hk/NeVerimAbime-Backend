import json
import sys
from collections import namedtuple
import requests
from django.http import JsonResponse
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            dummyIngredient = Ingredient.objects.create(name=request.data['name'],
                                                        description=request.data['description'],
                                                        caloriesPerUnit=request.data['caloriesPerUnit'],
                                                        unitType=request.data['unitType'],
                                                        recipeUuid=request.data['recipeUuid'],
                                                        fdcID=request.data['fdcID'],
                                                        amount=request.data['fdcID'])
            dummyIngredient.save()
            return Response("ok", status=HTTP_201_CREATED)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Ingredient throws error", status=HTTP_400_BAD_REQUEST)


def customNutrientDecoder(nutrientDict):
    return namedtuple('X', nutrientDict.keys())(*nutrientDict.values())

def nutrient_view(request):
    # TODO make configurative
    #todo handle null response
    url_parameter = request.GET.get("q")
    response = requests.get(
        'https://api.nal.usda.gov/fdc/v1/foods/search',
        # params={'api_key': '',
        params={'api_key': '',
                'dataType':'Foundation,Survey (FNDDS)',
                'query': url_parameter}
    )
    data = json.loads(response.text, object_hook=customNutrientDecoder)
    ingredients = data.foods
    data_dict = {"ingredients": ingredients}
    return JsonResponse(data=data_dict, safe=False)
