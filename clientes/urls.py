from django.urls import path

from clientes import views

app_name = "clientes"


urlpatterns = [
    path("", views.home, name="home"),
    path("pdf/", views.gerar_pdf, name="gerar_pdf"),
]
