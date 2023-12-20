from django import template

register = template.Library()

@register.filter
def remove_empty_lines(value):
    value = value.replace("\r", "")
    lines = value.split('\n')
    non_empty_lines = [line for line in lines if len(line) > 0]
    print(non_empty_lines)
    return non_empty_lines