# Created by keremocakoglu at 20-Jun-20
from rest_framework import serializers

from api.MealItem.serializers import MealItemSerializer
from api.Menu.models import Menu
from api.serializers import UserSerializer


class MenuSerializer(serializers.ModelSerializer):
    meal_items = MealItemSerializer(read_only=True, many=True)
    menu_owner=UserSerializer(read_only=True, many=False)
    class Meta:
        model = Menu
        fields = ['uuid','name','meal_items','menu_owner']
