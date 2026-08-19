from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..forms import MessageForm
from ..models import Message


# Create your views here.
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mail_service/message/message_list.html'

    def get_queryset(self):
        if self.request.user.has_perm("mail_service.view_message"):
            return super().get_queryset()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'mail_service/message/message_detail.html'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm("mail_service.view_message")


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_service/message/message_form.html'
    success_url = reverse_lazy("mail_service:message_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Users").exists()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_service/message/message_form.html'
    success_url = reverse_lazy("mail_service:message_list")

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'mail_service/message/message_confirm_delete.html'
    success_url = reverse_lazy("mail_service:message_list")

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user
