from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED

from api.CaloriesPerDay.models import CaloriesPerDay
from api.CaloriesPerDay.serializers import CaloriesPerDaySerializer
from api.models import  User
import sys, logging
from rest_framework.response import Response

from api.recipe.models import Recipe
import django

class CaloriesPerDayViewSet(viewsets.ModelViewSet):
    serializer_class = CaloriesPerDaySerializer
    queryset = CaloriesPerDay.objects.all()

    def create(self, request, *args, **kwargs):

        # logger = logging.getLogger('django')
        try:
            user = User.objects.get(id=request.user.id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            dummycalories = CaloriesPerDay.objects.create(user=user)
            recipe=Recipe.objects.get(uuid=request.data['recipeid'])
            dummycalories.gainedCalories=recipe.calories
            dummycalories.date=django.utils.timezone.now().replace(hour=0,
                                                minute=0,
                                                second=0,
                                                microsecond=0)
            dummycalories.recipes.add(recipe)
            dummycalories.save()

            return Response("success", status=HTTP_201_CREATED)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="CaloriesPerDay throws error", status=HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="addintocalories", detail=False, permission_classes=[permissions.IsAuthenticated])
    def addintocalories(self, request, *args, **kwargs):
        # logger = logging.getLogger('django')
        try:
            user = User.objects.get(id=request.user.id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            dummycalories = CaloriesPerDay.objects.get_or_create(user=user,
                                                                 date=django.utils.timezone.now().replace(hour=0,
                                                                     minute=0,
                                                                     second=0,
                                                                     microsecond=0))
            recipe = Recipe.objects.get(uuid=request.query_params['recipeid'])
            totalCalories =dummycalories[0].gainedCalories
            dummycalories[0].gainedCalories = recipe.calories +totalCalories
            dummycalories[0].save()
            dummycalories[0].recipes.add(recipe)
            dummycalories[0].save()
            return Response("success", status=HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="CaloriesPerDay throws error", status=HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="getuserconsumption", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getuserconsumption(self, request, *args, **kwargs):
        # logger = logging.getLogger('django')
        try:
            user = User.objects.get(id=request.user.id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            consumptionperday = CaloriesPerDay.objects.filter(user=user)
            cons_serializer = CaloriesPerDaySerializer(consumptionperday, many=True)
            return Response(cons_serializer.data, status=HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="CaloriesPerDay throws error", status=HTTP_400_BAD_REQUEST)