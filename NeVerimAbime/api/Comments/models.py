from django.db import models

# Create your models here.
from api.models import User
from api.recipe.models import Recipe
import uuid as uuid

class CommentString(models.Model):
    comments_string = models.CharField(max_length=1024, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=False)
    def __str__(self):
        return str(self.comments_string)[0:10]

    def get_comment_string(self):
        return str(self.comments_string)


class Comments(models.Model):
    # uuid = models.UUIDField(default=uuid.uuid4,
    #                         editable=False,
    #                         unique=False)
    comments = models.ManyToManyField(CommentString, related_name='comments')
    recipe = models.ForeignKey(Recipe, related_name='which_recipe', on_delete=models.SET_NULL, null=True)
    commented_user = models.ForeignKey(User, related_name='commented_user', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.recipe.name) + ": " + str(self.recipe.uuid)

    def save(self, *args, **kwargs):
        try:
            commentedObject = Comments.objects.get(recipe=self.recipe)
            if commentedObject.pk != None:
                commentedObject.comments.add(self.user)
            else:
                super(Comments, self).save(*args, **kwargs)
        except:
            super(Comments, self).save(*args, **kwargs)

    def get_all_comments(self):
        comments_list = []
        comments = self.comments.all()
        for comment in comments:
            comments_list.append(comment.get_comment_string())

        return comments_list

    # comments_list = {}
    # comments = self.comments.all()
    # for comment in comments:
    #     user = User.objects.get(id=self.commented_user.id)
    #     comments_list[comment.get_comment_string()] = user.name
    # return comments_list
