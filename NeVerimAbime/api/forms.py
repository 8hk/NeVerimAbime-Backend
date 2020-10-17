# Created by keremocakoglu at 24-May-20
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from api.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email','follower','following')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields