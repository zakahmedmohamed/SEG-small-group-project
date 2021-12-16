from django import forms
from .models import User,Club, Membership
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.forms import fields,widgets
from django.utils import timezone


class Log_in_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class SignUpForm(forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'username', 'new_password', 'password_confirmation', 'bio', 'statement', 'chess_xp']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Enter your bio'}),
            'statement': forms.Textarea(attrs={'placeholder': 'Enter your statement'}),
            "chess_xp": forms.NumberInput(attrs={'placeholder': 'Enter your chess experience level'}),
        }

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            bio=self.cleaned_data.get('bio'),
            statement=self.cleaned_data.get('statement'),
            chess_xp=self.cleaned_data.get('chess_xp'),
            password=self.cleaned_data.get('new_password'),
        )
        return user

class Create_A_Club_Form(forms.ModelForm):
    """Form to create a club."""

    class Meta:
        """Form options."""

        model = Club
        fields = ['name', 'description', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter the club name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter the club description'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter the club location'}),
        }

    def save(self):
        """Create a new club"""
        super().save(commit = False)
        club = Club.objects.create(
            name = self.cleaned_data.get('name'),
            description = self.cleaned_data.get('description'),
            location = self.cleaned_data.get('location'),
            created_at = timezone.now()
        )
        return club

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'statement','chess_xp']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Enter your bio'}),
            'statement': forms.Textarea(attrs={'placeholder': 'Enter your statement'}),
            "chess_xp": forms.NumberInput(attrs={'placeholder': 'Enter your chess experience level'}),
        }

class PasswordForm(forms.Form):
    """Form enabling users to change their password."""
    password = forms.CharField(label='Current password', widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}))
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}))

    def clean(self):
        """Clean the data and generate messages for any errors."""
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')
