import hashlib
from random import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from profileapp.models import ProfileUser

#forms
class UserRegisterForm(UserCreationForm):
    #Adding class attributes and placeholders to model fields 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'
            visible.field.widget.attrs['placeholder'] = visible.field.label
            visible.field.widget.attrs['required'] = 'required'

    class Meta:
        model = ProfileUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')


    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) == 0 or len(username) > 16:
            raise forms.ValidationError('Username length must be between 0 and 16 characters')
        return username
            
    def save(self):
        user = super(UserRegisterForm, self).save(commit=False)
        user.is_active = False
        salt = hashlib.sha512(str(random()).encode('utf8')).hexdigest()[:-33]
        user.activation_key = hashlib.sha512((f'{user.email}{salt}').encode('utf8')).hexdigest()
        return user
        
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'
            visible.field.widget.attrs['placeholder'] = visible.field.label
