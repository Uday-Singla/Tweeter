from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Post, Comment, Profile
from django.utils.translation import gettext_lazy as _



class UserRegistrationForm(UserCreationForm):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.SelectDateWidget())
    
    class Meta:
        model = Profile
        fields = ['dp', 'bio', 'city', 'dob',]
        labels = {
            'dp': _('Profile Picture'),
            'bio': _('Bio'),
            'city': _('City'),
            'dob': _('Date of Birth'),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', ]