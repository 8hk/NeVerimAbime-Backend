# Created by keremocakoglu at 01-Jun-20
import os

from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        data = form.initial_data
        if data['foodProvider'] == 'true':
            user.foodProvider = True
        else:
            user.foodProvider = False
        user.username = data['username']
        user.email = data['email']
        user.password = data['password1']
        user.set_password( data['password1'])
        # user.profile_image=data['profile_image']
        user.save()
        return user