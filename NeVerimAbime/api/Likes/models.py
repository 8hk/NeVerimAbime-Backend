import django
from django.db import models

# Create your models here.
from api.models import User
from api.recipe.models import Recipe


class Likes(models.Model):
    who_liked = models.ManyToManyField(User, related_name='who_liked')
    recipe = models.ForeignKey(Recipe, related_name='owner_recipe', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.recipe.name) + ": " + str(self.recipe.uuid)

    def save(self, *args, **kwargs):
        try:
            likedObject = Likes.objects.get(recipe=self.recipe)
            if likedObject.pk != None:
                likedObject.who_liked.add(self.user)
            else:
                super(Likes, self).save(*args, **kwargs)
        except:
            super(Likes, self).save(*args, **kwargs)