import django
from django.db import models

# Create your models here.
from api.models import User
from api.recipe.models import Recipe
import uuid as uuid

class CaloriesPerDay(models.Model):
    # date= models.DateField(default=django.utils.timezone.now(),unique=True,blank=False)
    date= models.DateField(default=django.utils.timezone.now().replace(hour=0, minute=0, second=0, microsecond=0),blank=False)
    gainedCalories = models.FloatField(default=0,blank=True)
    user = models.ForeignKey(User, related_name='owner_user', on_delete=models.SET_NULL, null=True)
    recipes = models.ManyToManyField(Recipe, related_name='recipe_calories_pd')
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=True)

    def __str__(self):
        return str(self.date)+ ": "+ self.user.get_user_email()
