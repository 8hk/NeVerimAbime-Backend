# Created by keremocakoglu at 10-Jun-20
from api.Comments.models import Comments, CommentString
from rest_framework import serializers


class CommentStringSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentString
        fields=('comments_string','uuid')

class CommentsSerializer(serializers.ModelSerializer):
    comments = CommentStringSerializer(read_only=True, many=True)
    class Meta:
        model = Comments
        fields = ("comments", "recipe","commented_user")


