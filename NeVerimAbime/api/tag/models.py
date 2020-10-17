from django.db import models

# Create your models here.
from api.recipe.models import Recipe


class Tag(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False,unique=True)
    recipes = models.ManyToManyField(Recipe, related_name='recipes')


    def __str__(self):
        return self.name