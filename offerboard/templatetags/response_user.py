from django import template

from offerboard.models import Order

register = template.Library()


@register.simple_tag(takes_context=True)
def response_user(context):
    """Предложения пользователя"""
    response = Order.objects.filter(offers__seller=context['request'].user).values_list('name',
                                                                                       flat=True)
    return response