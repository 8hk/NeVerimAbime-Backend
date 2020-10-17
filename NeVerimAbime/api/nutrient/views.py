from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .models import Nutrient
from .serializers import NutrientSerializer


class NutrientViewSet(viewsets.ModelViewSet):
    serializer_class = NutrientSerializer
    queryset = Nutrient.objects.all()
    # queryset = Nutrient.objects.none()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nutrient = serializer.save()
        return Response(data=serializer.data, status=HTTP_201_CREATED)
        # queryset= Nutrient.objects.filter(name="feef")
        # return queryset