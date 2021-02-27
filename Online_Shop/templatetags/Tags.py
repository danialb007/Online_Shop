from django.template import Library

register = Library()
@register.filter
def PriceFormat(value):
    value = str(value)
    result = ''
    for ind ,num in enumerate(reversed(value), start=1):
        result += num
        if ind == len(value):
            break
        if ind % 3 == 0:
            result += ','
    return result[::-1]
