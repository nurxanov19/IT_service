from django import forms
from django.contrib.auth.forms import UserCreationForm  # built-in class form to create a user registration. Creates user
from django.contrib.auth.models import User
from .models import Post, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)     # by default UserCreationForm has no email field so we add manually

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'title', 'description']


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.email = self.cleaned_data['email']
        profile.user.save()
        if commit:
            profile.save()
        return profile