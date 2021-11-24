from django import forms
from .models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.forms import fields,widgets


class Log_in_form(forms.Form):
    username = forms.CharField(label="Username: ")
    password = forms.CharField(label='Password: ', widget=forms.PasswordInput())


class SignUpForm(forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'statement', 'chess_xp']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Enter your bio'}), # needs to be resized properly
            'statement': forms.Textarea(attrs={'placeholder': 'Enter your statement'}) # needs to be resized properly
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
