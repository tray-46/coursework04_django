from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from ..models import MailingList, Client, DispatchAttempt


class DashboardView(TemplateView):
    template_name = 'mail_service/dashboard.html'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        dt_now = timezone.now()
        user = self.request.user

        if user.groups.filter(name="Users").exists():
            content["mailing_list_count"] = MailingList.objects.filter(owner=user).count()
            content["active_mailing_list_count"] = MailingList.objects.filter(owner=user, is_enable=True,
                                                                              dispatch_start__lte=dt_now,
                                                                              dispatch_end__gte=dt_now).count()
            content["clients_count"] = Client.objects.filter(owner=user).count()

            total_attempts = MailingList.objects.filter(owner=user)
            content["total_attempts"] = total_attempts.count()
            content["successful_attempts"] = total_attempts.filter(status=True).count()
            content["failed_attempts"] = total_attempts.filter(status=False).count()
        else:
            content["mailing_list_count"] = MailingList.objects.count()
            content["active_mailing_list_count"] = MailingList.objects.filter(is_enable=True,
                                                                              dispatch_start__lte=dt_now,
                                                                              dispatch_end__gte=dt_now).count()
            content["clients_count"] = Client.objects.count()

            content["total_attempts"] = DispatchAttempt.objects.count()
            content["successful_attempts"] = DispatchAttempt.objects.filter(status=True).count()
            content["failed_attempts"] = DispatchAttempt.objects.filter(status=False).count()
        return content
