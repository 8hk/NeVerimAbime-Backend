from django.contrib import admin

# Register your models here.
from api.MealItem.models import MealItem


@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    fields = ['uuid','name', 'recipe','amount','price','description',
              'meal_item_owner']
    search_fields = ['name','meal_item_owner']
    readonly_fields = ['uuid']


    def __str__(self):
        return self.name
