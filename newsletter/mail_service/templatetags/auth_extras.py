from django import template
from users.models import User

register = template.Library()


@register.filter(name="has_group")
def has_group(user: User, group_name: str) -> bool:
    """
    Returns True if the user belongs to the specified group,
    otherwise returns False.
    """
    if not user or user.is_anonymous:
        return False
    return bool(user.groups.filter(name=group_name).exists())
