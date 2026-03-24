from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms

User = get_user_model()

class SignUpForm(UserCreationForm):


    class Meta:
        model = User
        fields = ['first_name','last_name','username','city','date_of_birth','avatar','gender','bio','interested_in']

        widgets = {
            'city': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-danger'
            }),
        }



class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','city','date_of_birth','avatar','gender','bio','interested_in']

        widgets = {
            'avatar': forms.FileInput(),
            'city': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-danger'
        })}