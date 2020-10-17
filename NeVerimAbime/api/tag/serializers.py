# Created by keremocakoglu at 05-Jun-20
from api.recipe.serializers import RecipeSerializer
from rest_framework import serializers

from api.tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(read_only=True, many=True)

    class Meta:
        model = Tag
        fields = ("name", "recipes")
