import sys

from django.shortcuts import render

# Create your views here.
from api.Comments.models import Comments, CommentString
from api.Comments.serializers import CommentsSerializer
from api.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    def create(self, request, *args, **kwargs):
        # logger = logging.getLogger('django')
        try:
            user = User.objects.get(id=request.user.id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            comment = CommentString.objects.create(comments_string=request.data['comments'])
            comments = Comments.objects.get_or_create(recipe=request.data['recipe'],
                                                      commented_user=user)
            comments[0].comments.add(comment)
            return Response("success", status=HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Comments throws error", status=HTTP_400_BAD_REQUEST)
