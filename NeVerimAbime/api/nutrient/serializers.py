# Created by keremocakoglu at 15-May-20
from rest_framework import serializers
from api.nutrient.models import Nutrient
class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ("uuid", "name", "ingredientId","fdcId","fdcRank","fdcNumber","amount")
