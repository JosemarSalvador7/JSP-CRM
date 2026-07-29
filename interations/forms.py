from django import forms
from interations.models import Interaction

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        exclude = ["id", "created_by", "created_at", "updated_at"]
        widgets = {
            'type_interaction': forms.Select(attrs={'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contact': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'type_interaction': 'Tipo de Interação',
            'date_time': 'Data/Hora do contacto',
            'description': 'Descrição',
            'contact': 'Contato',
        }