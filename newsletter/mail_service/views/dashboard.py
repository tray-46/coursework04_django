from django.utils import timezone
from django.views.generic import TemplateView

from ..models import MailingList, Client


class DashboardView(TemplateView):
    template_name = 'mail_service/dashboard.html'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        dt_now = timezone.now()
        content["mailing_list_count"] = MailingList.objects.count()
        content["active_mailing_list_count"] = MailingList.objects.filter(dispatch_start__lte=dt_now,
                                                               dispatch_end__gte=dt_now).count()
        content["clients_count"] = Client.objects.count()
        return content
