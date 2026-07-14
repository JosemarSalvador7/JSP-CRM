from django.urls import path

from contacts import views

app_name = "contacts"


urlpatterns = [
    path("list/", views.list_contacts, name="list"),
    path('add/',views.add_contacts,name='add'),
     path('delete/<int:id>/',views.delete_contacts,name='delete'),
    path("pdf/", views.gerar_pdf, name="gerar_pdf"),
]
