from django import forms
from django.contrib.auth.models import User
from .models import Watch

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class WatchForm(forms.ModelForm):
    class Meta:
        model = Watch
        fields = ("name", "description", "cost", "image")
        labels = {
            "name": "Watch Name",
            "description": "Description",
            "cost": "Price",
            "image": "Image",
        }
