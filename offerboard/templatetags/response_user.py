from django import template

from offerboard.models import Order

register = template.Library()


@register.simple_tag(takes_context=True)
def response_user(context):
    """Предложения пользователя"""
    if context['request'].user.is_authenticated:
        response = Order.objects.filter(offers__seller=context['request'].user).values_list('name',
                                                                                       flat=True)
        return response
    else:
        pass