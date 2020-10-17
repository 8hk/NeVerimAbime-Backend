import logging
import os
import sys

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import requests
from rest_auth.app_settings import UserDetailsSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, viewsets, mixins, generics, permissions
from rest_framework.authtoken.models import Token
from . import models
from . import serializers

from .permissions import (
    AdminOrAuthorCanEdit,
)
from .models import (
    User,
)
from .serializers import (
    UserSerializer,
)


class MeViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    queryset = User.objects.none()
    # serializer_class = UserDetailsSerializer
    serializer_class = UserSerializer

    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (
        IsAuthenticated,
    )

    @action(methods=["get"], url_path="getusers", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getusers(self, request, *args, **kwargs):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)

    @action(methods=["post"], url_path="addnewfollower", detail=False, permission_classes=[permissions.IsAuthenticated])
    def addnewfollower(self, request, *args, **kwargs):
        # logger = logging.getLogger('django')
        try:
            user = User.objects.get(id=request.user.id)
            following = User.objects.get(id=request.data['id'])
            following.follower.add(user)
            user.following.add(following)
            return Response("success", status=HTTP_200_OK)

        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="error", status=HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="getuser", detail=False, permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def getuser(self, request, *args, **kwargs):
        user = User.objects.get(id=request.query_params['id'])
        user_serializer = UserSerializer(user, many=False)
        return Response(user_serializer.data)

    @action(methods=["get"], url_path="getfollowing", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getfollowing(self, request, *args, **kwargs):
        user = User.objects.get(id=request.query_params['id'])
        followings = user.following.all()
        return Response(followings)

    @action(methods=["put"], url_path="addprofilepicture", detail=False, permission_classes=[permissions.AllowAny])
    def addprofilepicture(self, request, *args, **kwargs):
        parser_classes = [FileUploadParser,]
        user = User.objects.get(username=str(request.data['user']))
        f = request.data['file']

        user.profile_image.save(os.path.basename(str(user.uuid)+'.png'), f, save=True)
        return Response("ok",status=HTTP_200_OK)

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class UserListView(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
