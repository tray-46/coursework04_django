from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..forms import MailingListForm
from ..models import MailingList


# Create your views here.
class MailingListListView(ListView):
    model = MailingList
    template_name = 'mail_service/mailing_list/mailing_list_list.html'


class MailingListDetailView(DetailView):
    model = MailingList
    template_name = 'mail_service/mailing_list/mailing_list_detail.html'


class MailingListCreateView(CreateView):
    model = MailingList
    form_class = MailingListForm
    template_name = 'mail_service/mailing_list/mailing_list_form.html'
    success_url = reverse_lazy("mail_service:mailing_list_list")


class MailingListUpdateView(UpdateView):
    model = MailingList
    form_class = MailingListForm
    template_name = 'mail_service/mailing_list/mailing_list_form.html'
    success_url = reverse_lazy("mail_service:mailing_list_list")


class MailingListDeleteView(DeleteView):
    model = MailingList
    template_name = 'mail_service/mailing_list/mailing_list_confirm_delete.html'
    success_url = reverse_lazy("mail_service:mailing_list_list")
