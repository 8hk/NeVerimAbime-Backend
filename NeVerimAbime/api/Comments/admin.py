from django.contrib import admin

# Register your models here.
from api.Comments.models import Comments, CommentString


@admin.register(CommentString)
class CommentStringAdmin(admin.ModelAdmin):
    fields = ['comments_string','uuid']
    readonly_fields = ['uuid']
    search_fields = ['comments_string']

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    fields = ['comments', 'recipe','commented_user']
    search_fields = ['recipe']
    autocomplete_fields = ['comments']