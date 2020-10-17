# Created by keremocakoglu at 10-Jun-20


# Created by keremocakoglu at 27-May-20
from rest_framework import serializers

from api.CaloriesPerDay.models import CaloriesPerDay
from api.Likes.models import Likes


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ("who_liked", "recipe")


