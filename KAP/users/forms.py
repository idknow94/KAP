from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Profile, AVATAR_CHOICES

User = get_user_model()


class EditProfileForm(forms.ModelForm):
    avatar = forms.ChoiceField(
        choices=AVATAR_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class CampionSignupForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@campion.edu.gr'):
            raise ValidationError("Only @campion.edu.gr emails are allowed.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email

    class Meta:
        model = User
        fields = ['username', 'email']
