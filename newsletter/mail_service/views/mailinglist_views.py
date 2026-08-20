import logging

from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from ..forms import MailingListForm
from ..models import MailingList
from ..services import send_mailinglist


logger = logging.getLogger(__name__)

# Create your views here.
class MailingListListView(LoginRequiredMixin, ListView):
    model = MailingList
    template_name = 'mail_service/mailinglist/mailinglist_list.html'

    def get_queryset(self):
        if self.request.user.has_perm("mail_service.view_client"):
            return super().get_queryset()
        return MailingList.objects.filter(owner=self.request.user)


class MailingListDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MailingList
    template_name = 'mail_service/mailinglist/mailinglist_detail.html'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm("mail_service.view_client")


class MailingListCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MailingList
    form_class = MailingListForm
    template_name = 'mail_service/mailinglist/mailinglist_form.html'
    success_url = reverse_lazy("mail_service:mailinglist_list")

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        logger.info(f"User '{user}' accessed MailingListCreateView via {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name="Users").exists()

    def form_valid(self, form):
        logger.info("MailingList form validation passed. Attempting database save.")
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        logger.info(f"Successfully created MailingList ID: {self.object.id}")
        return response

    def form_invalid(self, form):
        logger.warning(f"Failed MailingList creation attempt. Errors: {form.errors.as_json()}")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class MailingListUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingList
    form_class = MailingListForm
    template_name = 'mail_service/mailinglist/mailinglist_form.html'
    success_url = reverse_lazy("mail_service:mailinglist_list")

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class MailingListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingList
    template_name = 'mail_service/mailinglist/mailinglist_confirm_delete.html'
    success_url = reverse_lazy("mail_service:mailinglist_list")

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class MailingListSendView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        pk = self.kwargs['pk']
        mailinglist = get_object_or_404(MailingList, pk=pk)
        return mailinglist.owner == self.request.user

    def get(self, request, *args, **kwargs):
        print("1")
        pk = self.kwargs['pk']
        send_mailinglist(pk)
        messages.success(request, "Mailing list launched.")
        return HttpResponseRedirect(reverse("mail_service:mailinglist_detail", kwargs={"pk":pk}))

class MailingListDisableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "mail_service.can_disable_mailinglist"

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        if not self.request.user.has_perm("users.can_block_user"):
            return HttpResponseForbidden()

        mailinglist = mailinglist = get_object_or_404(MailingList, pk=pk)
        mailinglist.is_enable = not mailinglist.is_enable
        mailinglist.save()
        return HttpResponseRedirect(reverse("mail_service:mailinglist_detail", kwargs={"pk": pk}))
