from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import User


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: int) -> str:
        return f"{user.pk}{timestamp}{user.is_active}"


account_activation_token = AccountActivationTokenGenerator()
