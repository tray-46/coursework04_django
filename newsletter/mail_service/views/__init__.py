from .client_views import ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientUpdateView
from .dashboard import DashboardView
from .mailinglist_views import (
    MailingListCreateView,
    MailingListDeleteView,
    MailingListDetailView,
    MailingListDisableView,
    MailingListListView,
    MailingListSendView,
    MailingListUpdateView,
)
from .message_views import MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView, MessageUpdateView

__all__ = [
    "ClientListView",
    "ClientDetailView",
    "ClientCreateView",
    "ClientUpdateView",
    "ClientDeleteView",
    "DashboardView",
    "MailingListListView",
    "MailingListDetailView",
    "MailingListCreateView",
    "MailingListUpdateView",
    "MailingListDeleteView",
    "MailingListSendView",
    "MailingListDisableView",
    "MessageListView",
    "MessageDetailView",
    "MessageCreateView",
    "MessageUpdateView",
    "MessageDeleteView",
]
