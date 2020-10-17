# Created by keremocakoglu at 27-May-20
from rest_framework import serializers

from api.CaloriesPerDay.models import CaloriesPerDay
from api.recipe.serializers import RecipeSerializer
from api.serializers import UserSerializer


class CaloriesPerDaySerializer(serializers.ModelSerializer):
    recipes=RecipeSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True, many=False)
    class Meta:
        model = CaloriesPerDay
        fields = ("date", "gainedCalories","user","recipes","uuid")


