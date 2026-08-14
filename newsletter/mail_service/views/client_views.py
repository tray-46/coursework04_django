from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..forms import ClientForm
from ..models import Client


# Create your views here.
class ClientListView(ListView):
    model = Client
    template_name = 'mail_service/client/client_list.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mail_service/client/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mail_service/client/client_form.html'
    success_url = reverse_lazy("mail_service:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mail_service/client/client_form.html'
    success_url = reverse_lazy("mail_service:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mail_service/client/client_confirm_delete.html'
    success_url = reverse_lazy("mail_service:client_list")
