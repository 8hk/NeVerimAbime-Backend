from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    User,
)


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'name','caloriesLimitation','foodProvider','uuid']
    search_fields = ['name','email','username']
    autocomplete_fields = ['follower','following']
    readonly_fields = ['uuid']


admin.site.register(User, CustomUserAdmin)

