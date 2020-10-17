from django.contrib import admin

# Register your models here.
from api.recipe.models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ['name', 'uuid', 'preparation', 'ingredients',
              'user','cuisine','recipe_image','difficulty','prep_time',
              'calories']
    readonly_fields = ['uuid']
    search_fields = ['name','uuid','user','cuisine']
    autocomplete_fields = ['ingredients']