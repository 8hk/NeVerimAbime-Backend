from django.contrib import admin

# Register your models here.
from api.tag.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'recipes']
    search_fields = ['name']
    autocomplete_fields = ['recipes']