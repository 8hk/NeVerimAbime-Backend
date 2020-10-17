from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ModelSerializer,
)


User = get_user_model()


class FollowerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_image',
            'follower',
            'caloriesLimitation',
            'foodProvider',
            'following',
            'uuid'
        )


class UserSerializer(ModelSerializer):
    follower = FollowerSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_image',
            'follower',
            'caloriesLimitation',
            'foodProvider',
            'following',
            'uuid'
        )





class CustomRegisterSerializer(RegisterSerializer):
    foodProvider = serializers.BooleanField(
        required=True
    )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['foodProvider'] = self.validated_data.get('foodProvider', '')