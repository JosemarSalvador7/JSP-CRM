from django.urls import path
from task import views

app_name = "tasks"

urlpatterns = [
    path("list/", views.list_view, name="list"),
    path("retrieve/<int:id>/", views.retrieve_view, name="retrieve"),
    path("post/", views.post_view, name="post"),
    path("put/<int:id>/", views.put_view, name="put"),
    path("delete/<int:id>/", views.delete_view, name="delete"),
    path("pdf/", views.gerar_pdf_tasks, name="pdf"),
    path("pdf/<int:id>/", views.retrievepdf_task, name="retrievepdf"),
]