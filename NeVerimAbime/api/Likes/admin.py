from django.contrib import admin

# Register your models here.
from api.Likes.models import Likes


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    fields = ['who_liked', 'recipe']
    search_fields = ['recipe']
    autocomplete_fields = ['who_liked']