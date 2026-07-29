from django import forms
from task.models import Task
from django.contrib.auth.models import User
from contacts.models import Contact
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["id", "created_by", "created_at", "updated_at"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título da tarefa'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva a tarefa em detalhes...'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'DD/MM/AAAA'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control'
            }),
            'contact': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': _('Título'),
            'description': _('Descrição'),
            'due_date': _('Data de Vencimento'),
            'priority': _('Prioridade'),
            'status': _('Status'),
            'assigned_to': _('Atribuído a'),
            'contact': _('Contato'),
        }
        help_texts = {
            'title': _('Digite um título claro para a tarefa.'),
            'description': _('Descreva os detalhes e requisitos da tarefa.'),
            'due_date': _('Data limite para conclusão da tarefa.'),
            'priority': _('Prioridade da tarefa.'),
            'status': _('Status atual da tarefa.'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        # Adiciona classe 'form-control' a todos os campos
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'
            
            # Adiciona autofocus no primeiro campo
            if field_name == list(self.fields.keys())[0]:
                field.widget.attrs['autofocus'] = 'autofocus'
        
        # Filtra os contatos para mostrar apenas do usuário
        if user:
            self.fields['contact'].queryset = Contact.objects.filter(created_by=user)
            
        # Filtra usuários para atribuição
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        from django.utils import timezone
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError(_('A data de vencimento não pode ser no passado.'))
        return due_date