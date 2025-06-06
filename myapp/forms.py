import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post, Comment
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Напиши комментарий...'}),
        }

class CustomRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов.")
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Пароль не должен содержать спецсимволов.")
        return password