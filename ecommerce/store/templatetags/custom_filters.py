from django import template

register = template.Library()

@register.filter
def dictget(dictionary, key):
    """
    Get a value from a dictionary by key.
    Usage: {{ dictionary|dictget:key }}
    """
    if dictionary is None:
        return None

    # Convert key to string if it's not already
    str_key = str(key)

    # Try to get the value from the dictionary
    return dictionary.get(str_key, None)

@register.filter
def attr(obj, attr_name):
    """
    Get an attribute from an object.
    Usage: {{ object|attr:attribute_name }}
    """
    if obj is None:
        return ''

    # Try to get the attribute from the object
    try:
        # First try as a dictionary key
        if isinstance(obj, dict):
            return obj.get(attr_name, '')
        # Then try as an object attribute
        return getattr(obj, attr_name, '')
    except (TypeError, AttributeError):
        return ''
        
@register.filter
def product_image_url(image_field):
    """
    Get a safe image URL from a product image field.
    This handles both ImageField objects and legacy string paths.
    Usage: {{ product.image|product_image_url }}
    """
    if not image_field:
        return ''
        
    # Check if it's an ImageField object with a URL method
    if hasattr(image_field, 'url'):
        return image_field.url
        
    # If it's a string (backward compatibility)
    if isinstance(image_field, str):
        # If it already starts with http(s), return as is
        if image_field.startswith('http'):
            return image_field
        # Otherwise assume it's a relative path to MEDIA_URL
        return f'/media/{image_field}'
        
    # Fallback
    return ''
