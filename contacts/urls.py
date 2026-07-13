from django.urls import path

from contacts import views

app_name = "contacts"


urlpatterns = [
    path("", views.home, name="home"),
    path("pdf/", views.gerar_pdf, name="gerar_pdf"),
]
