# Created by keremocakoglu at 15-May-20
from rest_framework import serializers
from api.ingredient.serializers import IngredientSerializer
from api.recipe.models import Recipe
from api.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(read_only=True, many=True)
    user=UserSerializer(read_only=True,many=False)
    class Meta:
        model = Recipe
        fields = ("uuid", "name", "preparation", "ingredients",
                  "user","recipe_image",'difficulty','prep_time',
                  'calories','cuisine')
