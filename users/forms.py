from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True) #メールアドレスを必須にする文

    class Meta:
        model=get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'birth_date', 'gender', 'weight')
        labels = {
            'birth_date':'生年月日',
            'gender':'性別',
            'weight':'体重',
        }    

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField(required=True) #メールアドレスを必須にする文

    class Meta:
        model=get_user_model()
        fields = ( 'email', 'birth_date', 'gender', 'weight')
        labels = {
            'birth_date':'生年月日',
            'gender':'性別',
            'weight':'体重',
        }    