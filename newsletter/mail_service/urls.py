from django.urls import path

from .apps import MailServiceConfig

from . import views

app_name = MailServiceConfig.name

urlpatterns = [
    path('', views.ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/new/', views.ClientCreateView.as_view(), name='client_new'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_detete'),
]
