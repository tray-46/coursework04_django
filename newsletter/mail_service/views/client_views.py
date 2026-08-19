from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..forms import ClientForm
from ..models import Client


# Create your views here.
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mail_service/client/client_list.html'

    def get_queryset(self):
        if self.request.user.has_perm("mail_service.view_client"):
            return super().get_queryset()
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'mail_service/client/client_detail.html'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm("mail_service.view_client")


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mail_service/client/client_form.html'
    success_url = reverse_lazy("mail_service:client_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Users").exists()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mail_service/client/client_form.html'
    success_url = reverse_lazy("mail_service:client_list")

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mail_service/client/client_confirm_delete.html'
    success_url = reverse_lazy("mail_service:client_list")

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user
