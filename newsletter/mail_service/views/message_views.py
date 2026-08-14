from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..forms import MessageForm
from ..models import Message


# Create your views here.
class MessageListView(ListView):
    model = Message
    template_name = 'mail_service/message/message_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mail_service/message/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_service/message/message_form.html'
    success_url = reverse_lazy("mail_service:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_service/message/message_form.html'
    success_url = reverse_lazy("mail_service:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mail_service/message/message_confirm_delete.html'
    success_url = reverse_lazy("mail_service:message_list")
