from django import forms
from django.forms import fields,widgets
from clubs.models import User
from django.core.validators import RegexValidator 


#Forms will be made here

class Log_in_form(forms.Form):
    username = forms.CharField(label="Username: ")
    password = forms.CharField(label='Password: ', widget=forms.PasswordInput())
   
   
