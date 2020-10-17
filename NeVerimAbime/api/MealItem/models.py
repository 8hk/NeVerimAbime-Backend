from django.db import models
import uuid as uuid
# Create your models here.
from api.models import User
from api.recipe.models import Recipe


class MealItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=False)
    name = models.CharField(max_length=256, null=False, blank=False)
    recipe = models.ForeignKey(Recipe, related_name='which_meal', on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=0)
    price = models.FloatField(default=0)
    description = models.CharField(max_length=1024, null=True, blank=True)
    meal_item_owner = models.ForeignKey(User, related_name='meal_item_owner', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

