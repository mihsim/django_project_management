from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, PasswordChangeForm
from django.contrib.auth import authenticate

from .models import MyUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required, add valid email address.")

    class Meta:
        model = MyUser
        fields = ("email", "username", "password1", "password2")


class UserAuthenticationForm(forms.ModelForm):
    # widget=forms.PasswordInput - changes characters to ---> **************
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser  # Tells what fields will be available
        fields = ("email", "password", )  # Tells which fields will be shown.

    def clean(self):
        # clean method is available to every form that inherits from django.forms.ModelForm
        # claen(self) is run before form can do anything
        # so any logic writen here will be run first.
        if self.is_valid():  # False id password has a wrong format.
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class MyUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = MyUser
        fields = ("username", "email")
