from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import ClientForm
from ..models import Client


# Create your views here.
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mail_service/client/client_list.html"

    def get_queryset(self) -> QuerySet[Client]:
        user = self.request.user
        if user.is_authenticated:
            if user.has_perm("mail_service.view_client"):
                return super().get_queryset()
            return Client.objects.filter(owner=user)
        return Client.objects.none()


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = "mail_service/client/client_detail.html"

    def test_func(self) -> bool:
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm("mail_service.view_client")


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mail_service/client/client_form.html"
    success_url = reverse_lazy("mail_service:client_list")

    def test_func(self) -> bool:
        user = self.request.user
        if not user.is_authenticated:
            return False
        return user.groups.filter(name="Users").exists()

    def form_valid(self, form: ClientForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mail_service/client/client_form.html"
    success_url = reverse_lazy("mail_service:client_list")

    def test_func(self) -> bool:
        obj = self.get_object()
        return bool(obj.owner == self.request.user)


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = "mail_service/client/client_confirm_delete.html"
    success_url = reverse_lazy("mail_service:client_list")

    def test_func(self) -> bool:
        obj = self.get_object()
        return bool(obj.owner == self.request.user)
