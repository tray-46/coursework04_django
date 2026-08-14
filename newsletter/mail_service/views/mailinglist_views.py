from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from ..forms import MailingListForm
from ..models import MailingList
from ..services import send_mailinglist


# Create your views here.
class MailingListListView(ListView):
    model = MailingList
    template_name = 'mail_service/mailinglist/mailinglist_list.html'

    def get_queryset(self):
        return super().get_queryset()


class MailingListDetailView(DetailView):
    model = MailingList
    template_name = 'mail_service/mailinglist/mailinglist_detail.html'


class MailingListCreateView(CreateView):
    model = MailingList
    form_class = MailingListForm
    template_name = 'mail_service/mailinglist/mailinglist_form.html'
    success_url = reverse_lazy("mail_service:mailinglist_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingListUpdateView(UpdateView):
    model = MailingList
    form_class = MailingListForm
    template_name = 'mail_service/mailinglist/mailinglist_form.html'
    success_url = reverse_lazy("mail_service:mailing_list_list")


class MailingListDeleteView(DeleteView):
    model = MailingList
    template_name = 'mail_service/mailinglist/mailinglist_confirm_delete.html'
    success_url = reverse_lazy("mail_service:mailinglist_list")


class MailingListSendView(View):
    def get(self, request, *args, **kwargs):
        print("1")
        pk = self.kwargs['pk']
        send_mailinglist(pk)
        messages.success(request, "Mailing list launched.")
        return HttpResponseRedirect(reverse("mail_service:mailinglist_detail", kwargs={"pk":pk}))
