from django.db import models
import uuid as uuid


# Create your models here.
from api.MealItem.models import MealItem
from api.models import User


class Menu(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=False)
    name = models.CharField(max_length=256, null=False, blank=False)
    meal_items = models.ManyToManyField(MealItem, related_name='meal_item_menu')
    menu_owner = models.ForeignKey(User, related_name='menu_owner', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + ": "+ self.menu_owner.name
