from django import template

register = template.Library()

# -------------------------------
# Get dictionary value by key
# -------------------------------
@register.filter
def dict_get(dict_data, key):
    try:
        return dict_data.get(int(key))
    except:
        try:
            return dict_data.get(str(key))
        except:
            return None

# -------------------------------
# Multiply two values
# -------------------------------
@register.filter
def multiply(value, arg):
    try:
        return float(value) * int(arg)
    except:
        return 0

# -------------------------------
# For menu page: cart|get_item:item.id
# -------------------------------
@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(int(key), 0)
    except:
        return 0
