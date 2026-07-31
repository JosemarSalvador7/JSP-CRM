from django import forms
from contacts.models import Contact
from core.validators import validate_no_emoji
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        exclude = ["created_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

            if field.label != _("Atribuído a"):
                field.validators.append(
                    validate_no_emoji,
                )
