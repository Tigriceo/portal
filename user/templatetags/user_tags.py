from django import template

register = template.Library()


@register.filter()
def active(url, request):
    """активные ссылки в профиле"""
    if url[0:10] == request.get_full_path()[0:10]:
        return True
    else:
        return False
