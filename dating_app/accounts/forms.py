from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()

class SignUpForm(UserCreationForm):


    class Meta:
        model = User
        fields = ['username','city','date_of_birth','avatar','gender','bio']


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ['username','city','date_of_birth','avatar','gender','bio']