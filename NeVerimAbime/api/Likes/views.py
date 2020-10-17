import sys

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from api.Likes.models import Likes
from api.Likes.serializers import LikesSerializer
from api.models import User
from rest_framework.response import Response


class LikeViewSet(viewsets.ModelViewSet):

    serializer_class = LikesSerializer
    queryset = Likes.objects.all()

    def create(self, request, *args, **kwargs):

        # logger = logging.getLogger('django')
        try:
            user = User.objects.get(id=request.user.id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            liked = Likes.objects.create(who_liked=user,
                                                          recipe=request.data['recipe'],
                                                         )
            return Response("success", status=HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Likes throws error", status=HTTP_400_BAD_REQUEST)
