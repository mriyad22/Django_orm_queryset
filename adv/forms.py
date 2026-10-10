from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]



class RecruiterForm(forms.ModelForm):
    class Meta: 
        model = RecruiterModel
        fields = "__all__"
        exclude = ["user"]




class JobForm(forms.ModelForm):
    class Meta: 
        model = JobModel
        fields = "__all__"
        exclude = ["recruiter"]

        widgets = {
            'deadline' : forms.DateInput(attrs={'type':'date'})
        }