from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


#  AuthenticationForm
class LoginForm(forms.ModelForm):
    # username = forms.CharField(max_length=254,
    #                            widget=forms.TextInput(attrs=
    #                                                   {'class': 'form-control'}))
    #
    # password = forms.CharField(widget=forms.PasswordInput(attrs=
    #                                                       {'class': 'form-control',
    #                                                        'placeholder': 'Password'}))

    # username = forms.CharField(max_length=254,
    #                            widget=forms.TextInput())
    #
    # password = forms.CharField(widget=forms.PasswordInput())

    # class UserForm(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput)
        username = forms.CharField()

        class Meta:
            model = User
            fields = ['username', 'password']
