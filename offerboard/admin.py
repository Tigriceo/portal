from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Order, Offer


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Категории"""
    mptt_level_indent = 20
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Заявки - объявления"""
    list_display = ('id', 'name', 'slug', 'buyer', 'date_publication', 'payment_method')
    list_display_links = ("name",)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Предложение"""
    list_display = ('id', 'name', 'slug', 'order', 'seller', 'status')
    list_display_links = ("name",)
    prepopulated_fields = {'slug': ('name',)}