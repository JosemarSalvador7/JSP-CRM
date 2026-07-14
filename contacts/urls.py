from django.urls import path

from contacts import views

app_name = "contacts"


urlpatterns = [
    path("list/", views.list_contacts, name="list"),
    path("pdf/", views.gerar_pdf, name="gerar_pdf"),
]
