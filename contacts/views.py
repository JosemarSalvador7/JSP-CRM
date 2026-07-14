from django.db.models import Q
from django.shortcuts import get_object_or_404, render , redirect
from django.http import FileResponse
from fpdf import FPDF
from io import BytesIO

from contacts.form import ContactForm
from contacts.filters import ContactFilter
from contacts.models import Contact
# from clientes.models import Cliente
# Create your views here.


def gerar_pdf(requests):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Lista de Clientes")
    pdf.cell(w=85, h=30)  # type:ignore
    pdf.cell(w=60, h=0, txt="Clientes", ln=1, align="c")  # type:ignore
    pdf.set_font("Times", "", 12)
    pdf.cell(w=60, h=30, txt="", ln=1, align="c")  # type:ignore
    pdf_out = pdf.output(dest="S").encode("latin1")  # type:ignore
    return FileResponse(BytesIO(pdf_out), filename="clientes.pdf")


def list_contacts(request):
    contacts_qs = Contact.objects.all()
    contact_filter = ContactFilter(request.GET, queryset=contacts_qs)
    filtered_contacts = contact_filter.qs
    
    context = {
       
        'contactos': filtered_contacts,
        'filter': contact_filter,
        'contacts_count': filtered_contacts.count(),
        'contacts_with_email': filtered_contacts.filter(email__isnull=False).exclude(email='').count(),
        'contacts_without_email': filtered_contacts.filter(Q(email__isnull=True) | Q(email='')).count(),
        'contacts_with_company': filtered_contacts.filter(company__isnull=False).exclude(company='').count(),
    }
    return render(request, 'list_contacts.html', context)


    
def add_contacts(requests):
    form = ContactForm()
    if requests.method == "POST":
        form = ContactForm(requests.POST)
        
        if form.is_valid():
            form_add = form.save(commit=False)
            form_add.created_by = requests.user
            form.save()
            return redirect('contacts:add')
        else:
            print('invalido',form.errors)
    
    return render(requests,'add_contacts.html',{
         'form': form,
    })
    
def delete_contacts(requests,id):
    user = get_object_or_404(Contact,id=id)
    user.delete()
    return redirect('contacts:list')

