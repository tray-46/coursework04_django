from smtplib import SMTPAuthenticationError, SMTPException, SMTPRecipientsRefused

from django.conf import settings
from django.core import mail
from django.utils import timezone

from .models import DispatchAttempt, MailingList


def send_mailinglist(mailinglist_id: int) -> None:
    mailing_list = MailingList.objects.get(id=mailinglist_id)

    dt_now = timezone.now()
    if not mailing_list.dispatch_start <= dt_now <= mailing_list.dispatch_end:
        print("this mailing list is not active")
        return

    email_massage = mailing_list.message
    recipients_list = mailing_list.recipients.all()

    sent_successfully = 0
    sent_errors = 0
    dispatch_attempt_list = list()

    for recipient in recipients_list:
        dispatch_attempt = DispatchAttempt(mailing_list=mailing_list, attempt_dt=dt_now)
        try:
            sent_count = mail.send_mail(
                subject=email_massage.subject,
                message=email_massage.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            if sent_count == 1:
                sent_successfully += 1
                dispatch_attempt.status = True
        except ValueError as e:
            sent_errors += 1
            dispatch_attempt.smtp_response = f"Invalid header found. Error: {str(e)}"
        except SMTPAuthenticationError as e:
            sent_errors += 1
            if isinstance(e.smtp_error, bytes):
                err_msg = e.smtp_error.decode()
            else:
                err_msg = e.smtp_error
            dispatch_attempt.smtp_response = f"Auth failed. Code: {e.smtp_code}, Message: {err_msg}"
        except SMTPRecipientsRefused as e:
            sent_errors += 1
            dispatch_attempt.smtp_response = f"Rejected recipients: {e.recipients}"
        except SMTPException as e:
            sent_errors += 1
            dispatch_attempt.smtp_response = f"Smtp error occurred: {str(e)}"
        # dispatch_attempt.save()
        dispatch_attempt_list.append(dispatch_attempt)
    DispatchAttempt.objects.bulk_create(dispatch_attempt_list)
    print(f"Successfully sent: {sent_successfully}, errors occurred: {sent_errors}")
