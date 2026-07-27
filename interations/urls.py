from django.urls import path
from interations.views import (
    InteractionListView,
    InteractionCreateView,
    InteractionUpdateView,
    InteractionDelete,
)

urlpatterns = [
    path("interactions/", InteractionListView.as_view(), name="interaction-list"),
    path(
        "interactions/create/",
        InteractionCreateView.as_view(),
        name="interaction-create",
    ),
    path(
        "interactions/<int:pk>/update/",
        InteractionUpdateView.as_view(),
        name="interaction-update",
    ),
    path(
        "interactions/<int:pk>/delete/",
        InteractionDelete.as_view(),
        name="interaction-delete",
    ),
]
