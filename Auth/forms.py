from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User
from django.forms import ModelForm

class createNewUser(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class customerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude=['user']
