from django import template

from offerboard.models import Category

register = template.Library()


@register.inclusion_tag('include/category.html')
def menu_categories():
    """Вывод категорий"""
    return {"category": Category.objects.all()}