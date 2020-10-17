from django.contrib import admin

# Register your models here.
from api.Menu.models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    fields = ['uuid','name','meal_items','menu_owner']
    search_fields = ['name','menu_owner']
    readonly_fields = ['uuid']
    autocomplete_fields = ['meal_items']


    def __str__(self):
        return self.name
