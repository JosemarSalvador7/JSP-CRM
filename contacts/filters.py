import django_filters
from django import forms
from django_filters import CharFilter
from contacts.models import Contact
from django.utils.translation import gettext_lazy as _


class ContactFilter(django_filters.FilterSet):
    name = CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label=_("Nome"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    surname = CharFilter(
        field_name="surname",
        lookup_expr="icontains",
        label=_("Sobrenome"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = CharFilter(
        field_name="email",
        lookup_expr="icontains",
        label=_("Email"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    company = CharFilter(
        field_name="company",
        lookup_expr="icontains",
        label="Empresa",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    city = CharFilter(
        field_name="city",
        lookup_expr="icontains",
        label=_("Cidade"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Contact
        fields = ["name", "surname", "email", "company", "city"]
