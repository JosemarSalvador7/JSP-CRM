from django import forms
from opportunities.models import Opportunity
from django.utils.translation import gettext_lazy as _
from contacts.models import Contact
from django.contrib.auth.models import User


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        exclude = ["id", "created_by", "created_at", "updated_at"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o nome da oportunidade",
                }
            ),
            "value": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0.00", "step": "0.01"}
            ),
            "stage": forms.Select(attrs={"class": "form-control"}),
            "contact": forms.Select(attrs={"class": "form-control"}),
            "assigned_to": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "name": _("Nome da Oportunidade"),
            "value": _("Valor Estimado"),
            "stage": _("Estágio"),
            "contact": _("Contato"),
            "assigned_to": _("Atribuído a"),
        }
        help_texts = {
            "name": _("Digite um nome descritivo para a oportunidade."),
            "value": _("Informe o valor estimado da oportunidade."),
            "stage": _("Estágio atual da oportunidade no funil de vendas."),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(OpportunityForm, self).__init__(*args, **kwargs)

        # Adiciona classe 'form-control' a todos os campos
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                if "class" in field.widget.attrs:
                    field.widget.attrs["class"] += " form-control"
                else:
                    field.widget.attrs["class"] = "form-control"

            # Adiciona autofocus no primeiro campo
            if field_name == list(self.fields.keys())[0]:
                field.widget.attrs["autofocus"] = "autofocus"

        # Filtra os contatos para mostrar apenas do usuário
        if user:
            self.fields["contact"].queryset = Contact.objects.filter(created_by=user)

        # Filtra usuários para atribuição
        self.fields["assigned_to"].queryset = User.objects.filter(is_active=True)

    def clean_value(self):
        value = self.cleaned_data.get("value")
        if value and value < 0:
            raise forms.ValidationError(_("O valor não pode ser negativo."))
        return value
