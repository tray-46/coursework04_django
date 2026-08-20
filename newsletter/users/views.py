from django.core.cache import cache
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils import cache
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.models import Group
from .tokens import account_activation_token
from .forms import LoginForm, RegisterForm
from .models import User


# Create your views here.
class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("users:registration_pending")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        users_groups, _ = Group.objects.get_or_create(name="Users")
        user.groups.add(users_groups)

        current_site = get_current_site(self.request)
        mail_subject = "Activate your account"
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        message = render_to_string("users/activation_email.html", {"user": user, "domain": current_site.domain,
                                                                   "uid": uid, "token": token, })
        email = EmailMessage(mail_subject, message, "no-reply@it.ivc.vsmpo.ru", to=[user.email])
        email.send()
        return redirect(self.success_url)

class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print(f"activation: {user}, {uid}, {token}, {account_activation_token.check_token(user, token)}")

        if user is not None and account_activation_token.check_token(user, token):
            print(f"activation: {user}")
            user.is_active = True
            user.save()
            return redirect("users:login")
        else:
            return redirect("users:login")

class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = LoginForm


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = "users.view_user"
    template_name = "users/list.html"

    def get_queryset(self):
        cache_key = "service_users"
        service_users = cache.get(cache_key)

        if service_users:
            return service_users

        service_users =User.objects.filter(groups__name="Users")
        cache.set(cache_key, service_users, 60 * 5)
        return service_users


class UserBlockView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """"""
    permission_required = "users.can_block_user"

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        if not self.request.user.has_perm("users.can_block_user"):
            return HttpResponseForbidden()

        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        return redirect("users:user_list")

