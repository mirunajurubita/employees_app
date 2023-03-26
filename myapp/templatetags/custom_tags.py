from django import template

register = template.Library()
@register.filter
def seconds_to_hhmmss(seconds):
    print(type(seconds))
    total_seconds = seconds.total_seconds() * 1000000
    print(total_seconds)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    secs = int(total_seconds % 60)
    ## la primul era 2d
    return '{:01d} hours {:02d} minutes {:02d} seconds'.format(hours, minutes, secs)