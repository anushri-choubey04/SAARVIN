from django import template
from django.db import models

register = template.Library()

@register.filter
def safe_image_url(image_field):
    """
    Safely get the URL of an ImageField.
    Returns the URL if the field has a file, otherwise returns None.
    """
    try:
        if image_field and hasattr(image_field, 'url') and image_field.name:
            return image_field.url
    except (ValueError, AttributeError):
        pass
    return None

@register.filter
def has_image(image_field):
    """
    Check if an ImageField has an actual file associated with it.
    """
    try:
        return image_field and hasattr(image_field, 'name') and image_field.name
    except (ValueError, AttributeError):
        return False
