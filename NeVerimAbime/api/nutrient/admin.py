from django.contrib import admin

# Register your models here.
from api.nutrient.models import Nutrient

@admin.register(Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    fields = ['name', 'uuid', 'unitName', 'ingredientId','fdcId' , 'fdcRank', 'fdcNumber','amount']
    readonly_fields = ['uuid']
    search_fields = ['name','ingredientId','fdcId']