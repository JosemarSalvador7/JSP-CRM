from django.urls import path
from opportunities import views

app_name = "opportunities"

urlpatterns = [
    path("list/", views.list_view, name="list"),
    path("kanban/", views.kanban_view, name="kanban"),
    path("retrieve/<int:id>/", views.retrieve_view, name="retrieve"),
    path("post/", views.post_view, name="post"),
    path("put/<int:id>/", views.put_view, name="put"),
    path("delete/<int:id>/", views.delete_view, name="delete"),
    path("update-stage/<int:id>/", views.update_stage_view, name="update_stage"),
    path("pdf/", views.gerar_pdf_opportunities, name="pdf"),
    path("pdf/<int:id>/", views.retrievepdf_opportunity, name="retrievepdf"),
]
