from django import forms
from blogs import models


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'image']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EditMyProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'first_name', 'last_name', 'image']
