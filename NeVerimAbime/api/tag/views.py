import sys

from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from api.tag.models import Tag
from api.tag.serializers import TagSerializer
from rest_framework import viewsets, serializers, permissions


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            tag=Tag.objects.get_or_create(name=request.data['name'])
            tag.recipes.add(request.data['recipe'])
            tag.save()
            return Response(data="ok", status=HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Tag throws error", status=HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="search", detail=False, permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def search(self, request, *args, **kwargs):
        try:
            tags = Tag.objects.filter(name=request.query_params['query'])
            tag_serializer = TagSerializer(tags, many=True)
            return Response(tag_serializer.data,status=HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Tag throws error", status=HTTP_400_BAD_REQUEST)
