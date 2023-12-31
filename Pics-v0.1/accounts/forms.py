from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import (
    validate_password,
    password_validators_help_text_html,
)
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        validators=[validate_password],
        help_text=password_validators_help_text_html)
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
            'is_staff',
            'account_tier'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password',
            'username',
            'account_tier',
            'user_permissions',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined'
        )
