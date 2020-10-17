from django.contrib import admin

# Register your models here.
from api.ingredient.models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = ['name', 'uuid', 'description', 'caloriesPerUnit','unitType', 'nutrients','recipeUuid','fdcID','amount']
    readonly_fields = ['uuid']
    search_fields = ['name','uuid','fdcID','recipeUuid']
    autocomplete_fields = ['nutrients']