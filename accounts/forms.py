from django import forms
from django.contrib.auth.models import User


class CastroUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()


class FormLogin(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()
