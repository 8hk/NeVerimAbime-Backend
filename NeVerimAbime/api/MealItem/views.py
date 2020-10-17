from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response

from api.MealItem.models import MealItem
from api.MealItem.serializers import MealItemSerializer
import sys

from api.models import User
from api.recipe.models import Recipe


class MealItemViewSet(viewsets.ModelViewSet):

    serializer_class = MealItemSerializer
    queryset = MealItem.objects.all()

    def create(self, request, *args, **kwargs):
        # logger = logging.getLogger('django')
        try:
            user = User.objects.get(id=request.user.id)
            recipe = Recipe.objects.get(uuid=request.data['recipe'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            mealitem= MealItem.objects.create(
                name=request.data['name'],
                recipe=recipe,
                amount=request.data['amount'],
                price=request.data['price'],
                description=request.data['description'],
                meal_item_owner=user,
            )
            return Response("success", status=HTTP_201_CREATED)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="MealItem throws error", status=HTTP_400_BAD_REQUEST)
