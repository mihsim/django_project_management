from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth import authenticate

from .models import MyUser



from django.contrib import auth


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required, add valid email address.")

    class Meta:
        model = MyUser
        fields = ("email", "username", "password1", "password2")


class UserAuthenticationForm(forms.ModelForm):
    # widget=forms.PasswordInput - changes characters to ---> **************
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser  # Tells what fields will be available
        fields = ("email", "password1", )  # Tells which fields will be shown.

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ("username", "email", "password")

    def clean_password(self):
        return self.initial["password"]
