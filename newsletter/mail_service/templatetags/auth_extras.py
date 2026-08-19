from django import template

register = template.Library()

@register.filter(name="has_group")
def has_group(user, group_name):
    """
    Returns True if the user belongs to the specified group,
    otherwise returns False.
    """
    if not user or user.is_anonymous:
        return False
    return user.groups.filter(name=group_name).exists()
