from django import template

from offerboard.models import Order, Offer

register = template.Library()


# @register.simple_tag(takes_context=True)
# def response_user(context):
#     """Предложения пользователя"""
#     if context['request'].user.is_authenticated:
#         response = Order.objects.filter(offers__seller=context['request'].user).values_list('name',
#                                                                                        flat=True)
#         return response
#     else:
#         pass


@register.simple_tag(takes_context=True)
def count_offer_user(context, pk):
    """Разрешаю сделать предложение, если меньше 3-х отклоненых предложений на одну заявку.
    Если это не его заявка, и если на заявку еще не отреагировали."""
    if context['request'].user.is_authenticated:
        user = context['request'].user
        count_offer = Offer.objects.filter(order=pk, seller=user).filter(status='reject').count()
        response = Offer.objects.filter(order=pk, seller=user).exclude(status="reject")
        order_user = Order.objects.filter(id=pk)[0].buyer

        if count_offer >= 3 or response or user == order_user:
            return 'no'
        else:
            return 'yes'
    else:
        pass