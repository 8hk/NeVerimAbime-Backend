from django.contrib import admin

# Register your models here.
from api.CaloriesPerDay.models import CaloriesPerDay


@admin.register(CaloriesPerDay)
class CaloriesPerDayAdmin(admin.ModelAdmin):
    fields = ['date', 'gainedCalories' ,'user','recipes','uuid']
    readonly_fields = ['uuid']
    search_fields = ['date','user']
    autocomplete_fields = ['recipes']