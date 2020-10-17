import enum

from django.db import models
import uuid as uuid

# Create your models here.
from api.ingredient.models import Ingredient
from api.models import User

DIFFICULTY_LEVELS = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
)

Cusines =[
"Turkish Food","Algerian Food","American Food","Belgian Foods","Brazilian Food","British Food","Cajun Food","Canadian Food","Chinese Food","Cuban Food","Egyptian Food","French Food","German Food","Greek Food","Haitian Food","Hawaiian Food","Indian Food","Irish Food","Italian Food","Japanese Food","Jewish Food","Kenyan Food","Korean Food","Latvian Food","Libyan Food","Mexican Food","Mormon Food","Nigerian Food","Peruvian Food","Polish Food","Portuguese Food","Russian Food","Salvadorian Food","Scottish Food","Spanish Food","Swedish Food","Tahitian Food","Thai Food","Tibetan Food","Welsh Food"
]

class Recipe(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    preparation = models.CharField(max_length=1024, null=True, blank=True)
    # picture = models.FileField()
    difficulty = models.CharField(choices=DIFFICULTY_LEVELS, max_length=10,default="Easy")
    prep_time = models.PositiveIntegerField(default=20,null=False, blank=False)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredients')
    user=models.ForeignKey(User, related_name='owner',on_delete=models.SET_NULL,null=True)
    cuisine=models.CharField(max_length=256,null=True,blank=True)
    recipe_image = models.ImageField(upload_to="recipe_image", blank=True, null=True)
    calories = models.FloatField(blank=False, default=0)
    # likes =models.IntegerField(default=0,null=False,blank=False)



    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Recipe, self).save(*args, **kwargs)

    def get_all_objects(self):
        queryset = Recipe.objects.all()
        return queryset