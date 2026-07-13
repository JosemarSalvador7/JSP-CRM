from django.shortcuts import render
from django.http import FileResponse
from fpdf import FPDF
from io import BytesIO
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


def home(requests):

    return render(
        requests,
        "home.html",
    )
