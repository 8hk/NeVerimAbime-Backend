# Created by keremocakoglu at 15-May-20
from rest_framework import serializers
from api.ingredient.models import Ingredient
from api.nutrient.serializers import NutrientSerializer
class IngredientSerializer(serializers.ModelSerializer):
    nutrients = NutrientSerializer(read_only=True, many=True)
    class Meta:
        model = Ingredient
        fields = ("uuid", "name", "description", "caloriesPerUnit", "unitType", "nutrients", "recipeUuid","fdcID","amount")


