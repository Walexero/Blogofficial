from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author','date_posted', 'slug']

class RegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['commenter','post','reply']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Enter Text', 'rows':4, 'cols':'50'})
        }
