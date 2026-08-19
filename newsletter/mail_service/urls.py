from django.urls import path

from .apps import MailServiceConfig

from . import views

app_name = MailServiceConfig.name

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),

    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/new/', views.ClientCreateView.as_view(), name='client_new'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/new/', views.MessageCreateView.as_view(), name='message_new'),
    path('messages/<int:pk>/edit/', views.MessageUpdateView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),

    path('mailinglists/', views.MailingListListView.as_view(), name='mailinglist_list'),
    path('mailinglists/<int:pk>/', views.MailingListDetailView.as_view(), name='mailinglist_detail'),
    path('mailinglists/new/', views.MailingListCreateView.as_view(), name='mailinglist_new'),
    path('mailinglists/<int:pk>/edit/', views.MailingListUpdateView.as_view(), name='mailinglist_edit'),
    path('mailinglists/<int:pk>/delete/', views.MailingListDeleteView.as_view(), name='mailinglist_delete'),
    path('mailinglists/<int:pk>/send/', views.MailingListSendView.as_view(), name='mailinglist_send'),
path('mailinglists/<int:pk>/disable/', views.MailingListDisableView.as_view(), name='mailinglist_disable'),
]
