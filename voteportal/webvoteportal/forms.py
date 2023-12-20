#from django.forms import modalForm
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class createUserForm(UserCreationForm):
      email = forms.EmailField(max_length=200)
      first_name = forms.CharField(max_length=200)
      last_name = forms.CharField(max_length=200)
      
      class Meta:

            model = User
            fields = ['username','first_name','last_name','email','password1','password2']

class ProfileForm(forms.ModelForm):
      regid = forms.CharField(max_length=200)
      class Meta:
            model = Profile
            fields = ['regid','voted']