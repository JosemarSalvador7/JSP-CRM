from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.http import FileResponse, HttpResponse
from fpdf import FPDF
from io import BytesIO
from django.contrib import messages
from contacts.form import ContactForm
from contacts.filters import ContactFilter
from contacts.models import Contact
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

# Permissoes
from rolepermissions.decorators import has_permission_decorator


@has_permission_decorator("view_contact_pdf")
@login_required()
def retrievepdf(request, id):
    if request.user.profile.role == "G":
        contact = get_object_or_404(
            Contact,
            Q(
                id=id,
            ),
        )
    elif request.user.profile.role == "V":
        contact = get_object_or_404(Contact, Q(id=id, assigned_to=request.user))
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", "B", 24)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Lista de Clientes")
    pdf.cell(w=60, h=30)  # type:ignore
    pdf.cell(
        w=60,
        h=0,
        txt=f"{contact.name.capitalize()} {contact.surname.capitalize()}",
        ln=1,
        align="c",
    )  # type:ignore assigned_to
    pdf.set_font("Times", "", 12)
    pdf.cell(w=10, h=10, txt="", ln=1, align="c")  # type:ignore
    pdf.set_font("Times", "B", 20)
    pdf.cell(w=10, h=10, txt="Informações Pessoais", ln=1, align="c")
    pdf.set_font("Times", "B", 12)
    # Nome
    pdf.cell(
        w=20,
        h=10,
        txt="Nome:",
        ln=0,
        align="c",
    )
    pdf.set_font("Times", "", 12)
    pdf.cell(w=20, h=10, txt=f"{contact.name.capitalize()}", ln=1, align="c")
    # Sobrenome
    pdf.set_font("Times", "B", 12)
    pdf.cell(
        w=30,
        h=10,
        txt="Sobrenome:",
        ln=0,
        align="c",
    )
    pdf.set_font("Times", "", 12)
    pdf.cell(w=20, h=10, txt=f"{contact.surname.capitalize()}", ln=1)
    # Telefone
    pdf.set_font("Times", "B", 12)
    pdf.cell(
        w=40,
        h=10,
        txt="Telefone:",
        ln=0,
        align="c",
    )
    pdf.set_font("Times", "", 12)
    pdf.cell(w=40, h=10, txt=f"{contact.phone}", ln=1, align="c")
    # E-mail
    pdf.set_font("Times", "B", 12)
    pdf.cell(
        w=40,
        h=10,
        txt="E-mail:",
        ln=0,
        align="c",
    )
    pdf.set_font("Times", "", 12)
    pdf.cell(w=40, h=10, txt=f"{contact.email or _('Não informado')}", ln=1, align="c")
    # Empresa
    pdf.set_font("Times", "B", 12)
    pdf.cell(
        w=40,
        h=10,
        txt="Empresa:",
        ln=0,
    )
    pdf.set_font("Times", "", 12)
    pdf.cell(
        w=40,
        h=10,
        txt=f"{contact.company or _('Não informado')}",
        ln=1,
    )
    pdf.set_font("Times", "B", 12)
    # Cargo
    pdf.cell(
        w=40,
        h=10,
        txt="Cargo:",
        ln=0,
        align="c",
    )
    pdf.set_font("Times", "", 12)
    pdf.cell(
        w=40,
        h=10,
        txt=f"{contact.job_title or _('Não informado')}",
        ln=1,
        align="c",
    )
    # Vendedor Responsavel
    pdf.set_font("Times", "B", 12)
    pdf.cell(
        w=50,
        h=10,
        txt="Vendedor responsável:",
        ln=0,
        align="c",
    )
    pdf.set_font("Times", "", 12)
    pdf.cell(
        w=40,
        h=10,
        txt=f"{contact.assigned_to or _('Não informado')}",
        ln=1,
        align="c",
    )
    pdf_contact = pdf.output(dest="S").encode("latin1")  # type: ignore
    return FileResponse(
        BytesIO(pdf_contact), filename=f"{contact.name} {contact.surname}.pdf"
    )


@has_permission_decorator("view_contacts_pdf")
@login_required()
def gerar_pdf(request):
    contacts = Contact.objects.all().filter(assigned_to=request.user)
    pdf = FPDF()
    pdf.add_page(orientation="landscape")
    pdf.set_font("Times", "B", 24)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Lista de Clientes")
    pdf.cell(w=120, h=30)  # type:ignore
    pdf.cell(w=60, h=0, txt="Contactos", ln=1, align="c")  # type:ignore assigned_to
    pdf.set_font("Times", "", 12)
    pdf.cell(w=10, h=10, txt="", ln=1, align="c")  # type:ignore
    pdf.cell(w=60, h=10, txt="Nome Completo", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="Telefone", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="E-mail", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="Empresa", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="Cargo", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="Vendedor responsável", border=1, ln=1, align="c", fill=1)

    for i in contacts:
        pdf.cell(
            w=60,
            h=10,
            txt=f"{i.name.capitalize()} {i.surname.capitalize()} ",
            border=1,
            ln=0,
            align="c",
        )
        pdf.cell(w=40, h=10, txt=f"{i.phone}", border=1, ln=0, align="c")
        pdf.cell(
            w=40,
            h=10,
            txt=f"{i.email or _('Não informado')}",
            border=1,
            ln=0,
            align="c",
        )
        pdf.cell(
            w=40,
            h=10,
            txt=f"{i.company or _('Não informado')}",
            border=1,
            ln=0,
            align="c",
        )
        pdf.cell(
            w=40,
            h=10,
            txt=f"{i.job_title or _('Não informado')}",
            border=1,
            ln=0,
            align="c",
        )
        pdf.cell(
            w=40,
            h=10,
            txt=f"{i.assigned_to or _('Não informado')}",
            border=1,
            ln=1,
            align="c",
        )

    pdf_out = pdf.output(dest="S").encode("latin1")  # type:ignore
    return FileResponse(BytesIO(pdf_out), filename="contactos.pdf")


@login_required()
def list_contacts(request):
    print()
    if request.user.profile.role == "G":
        contacts_qs = Contact.objects.all()
    elif request.user.profile.role == "V":
        contacts_qs = Contact.objects.only(
            "id", "name", "surname", "phone", "email", "company", "job_title"
        ).filter(assigned_to=request.user)

    contact_filter = ContactFilter(request.GET, queryset=contacts_qs)
    filtered_contacts = contact_filter.qs

    context = {
        "contactos": filtered_contacts,
        "filter": contact_filter,
        "contacts_count": filtered_contacts.count(),
        "contacts_with_email": filtered_contacts.filter(email__isnull=False)
        .exclude(email="")
        .count(),
        "contacts_without_email": filtered_contacts.filter(
            Q(email__isnull=True) | Q(email="")
        ).count(),
        "contacts_with_company": filtered_contacts.filter(company__isnull=False)
        .exclude(company="")
        .count(),
    }
    return render(request, "list_contacts.html", context)


@has_permission_decorator("add_contact")
@login_required()
def add_contacts(requests):
    form = ContactForm()
    if requests.method == "POST":
        form = ContactForm(requests.POST)

        if form.is_valid():
            form_add = form.save(commit=False)
            form_add.created_by = requests.user
            form.save()
            messages.success(requests, _("Contacto Adicionado com sucesso"))
            return redirect("contacts:list")
        else:
            messages.error(requests, _("Erro a adicionar Contacto"))
            return render(
                requests,
                "add_contacts.html",
                {
                    "form": form,
                },
            )

    return render(
        requests,
        "add_contacts.html",
        {
            "form": form,
        },
    )


@has_permission_decorator("delete_contact")
@login_required()
def delete_contacts(requests, id):
    # TODO: caso erro a elimiar mostrar mensaguem de contecto associado
    try:
        contact = get_object_or_404(Contact, id=id)
        contact.delete()
    except Exception as e:
        return HttpResponse(e)
    messages.success(requests, _("Contacto Eliminado com sucesso"))
    return redirect("contacts:list")


@login_required()
def retrieve_contact(requests, id):

    contact = get_object_or_404(Contact, id=id)
    return render(
        requests,
        "retrieve_contact.html",
        {
            "form": 1,
            "contact": contact,
        },
    )


@has_permission_decorator("update_contact")
@login_required()
def update_contact(requests, id):
    contact = get_object_or_404(Contact, id=id)
    if requests.method == "POST":
        form = ContactForm(requests.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(requests, _("Editado com sucesso"))
            return redirect(f"/pt/contacts/retrieve/{id}")
        messages.error(requests, _("Erro a Editar Contacto"))
        return redirect(f"/pt/contacts/retrieve/{id}")
    return render(
        requests,
        "update_contact.html",
        {
            "form": ContactForm(instance=contact),
            "contact": contact,
        },
    )
