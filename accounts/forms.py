from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CastroUser(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()


class UserForm(forms.Form):
    avatar = forms.ImageField(
        required=False,
        label=_("Foto"),
        help_text=_("Adicone uma foto para ajudar na identificação"),
    )
    username = forms.CharField(
        max_length=255,
        label=_("Username"),
        required=True,
        help_text=_("Adicione um nome de usuário único para identificar sua conta."),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Password"),
        min_length=8,
        required=True,
        help_text=_(
            "Adicione uma senha forte, com letras, números e caracteres especiais."
        ),
    )
    role = forms.ChoiceField(
        choices=(("V", "Vendedor"), ("G", "Gerente")),
        label=_("Cargo"),
        required=True,
        help_text=_(
            "Selecione o cargo do usuário, que determinará suas permissões e responsabilidades dentro do sistema."
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        help_text=_(
            "Adicione um email válido para receber notificações e recuperar sua senha."
        ),
    )

    class Meta:
        abstract = True


class RegisterUserForm(UserForm): ...


class EditUserForm(UserForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label=_("Password"),
        min_length=8,
        required=False,
        help_text=_("Mantenha o campo vazio para manter a senha atual."),
    )
    avatar = forms.ImageField(
        required=False,
        label=_("Foto"),
        help_text=_("Mantenha o campo vazio para manter a foto atual."),
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].required = False

        # Adiciona classe form-control a todos os campos existentes
        for field_name, field in self.fields.items():
            if field_name not in ["password", "avatar"]:
                if hasattr(field.widget, "attrs"):
                    field.widget.attrs["class"] = "form-control"


class FormLogin(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()
