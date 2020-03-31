from django import forms

from .models import Order, Offer


class OrderForm(forms.ModelForm):
    """Создание заявки"""
    class Meta:
        model = Order
        fields = ['photo', 'name', "description", 'price_min', 'price_max', 'date_validity', 'payment_method']


class OfferForm(forms.ModelForm):
    """Создание предложения"""
    class Meta:
        model = Offer
        fields = ['name', 'description', 'price_min', 'photo']


class InactiveFilterForm(forms.Form):
    """Форма для фильтрации неактивных заявок и предложений"""
    min_data = forms.DateField(required=False)
    max_data = forms.DateField(required=False)

