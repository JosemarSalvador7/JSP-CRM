from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from interations.models import Interaction


class InteractionListView(ListView):
    model = Interaction
    template_name = "list_interaction.html"
    context_object_name = "interactions"


class InteractionCreateView(CreateView):
    model = Interaction
    template_name = "create_interaction.html"
    fields = ["type_interaction", "date_time", "description", "contact"]
    success_url = reverse_lazy("interaction-list")


class InteractionUpdateView(UpdateView):
    model = Interaction
    template_name = "update_interaction.html"
    fields = ["type_interaction", "date_time", "description", "contact"]
    success_url = reverse_lazy("interaction-list")


class InteractionDelete(DeleteView):
    model = Interaction
    template_name = "delete_interaction.html"
    success_url = reverse_lazy("interaction-list")
