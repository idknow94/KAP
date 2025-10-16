from django import forms
from .models import Issue, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CampionSignupForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@campion.edu.gr'):
            raise ValidationError("Only @campion.edu.gr emails are allowed.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issue title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the issue'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'text': ''  # removes "Text:" label
        }
