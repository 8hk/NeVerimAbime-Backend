from django.db import models
import uuid as uuid

# Create your models here.
from api.nutrient.models import Nutrient


class Ingredient(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(default="",max_length=1024, null=True, blank=True)
    caloriesPerUnit = models.FloatField(default=0)
    unitType = models.CharField(default="",max_length=256, null=False, blank=False)
    nutrients = models.ManyToManyField(Nutrient, related_name='nutrients')
    recipeUuid = models.CharField(default="",max_length=256, null=False, blank=False)
    fdcID = models.IntegerField(default=0,null=False,blank=False)
    amount = models.FloatField(default=0)


    def save(self, *args, **kwargs):
        if len(self.name) > 256:
            raise ValueError('Name length cant exceed 256 character')
        if len(self.description) > 1024:
            raise ValueError('Description length cant exceed 1024 character')
        super(Ingredient, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_all_objects(self):
        queryset = Ingredient.objects.all()
        return queryset
