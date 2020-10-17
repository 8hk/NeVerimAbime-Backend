# Created by keremocakoglu at 20-Jun-20

from rest_framework import serializers

from api.MealItem.models import MealItem
from api.recipe.serializers import RecipeSerializer


class MealItemSerializer(serializers.ModelSerializer):
    recipe= RecipeSerializer(read_only=True, many=False)
    class Meta:
        model = MealItem
        fields = ['name', 'recipe', 'amount',
                  'price', 'description',
                  'meal_item_owner']
