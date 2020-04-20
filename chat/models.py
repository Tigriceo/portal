from django.db import models
from django.contrib.auth.models import User

from offerboard.models import Offer


class RoomChat(models.Model):
    """Комната чата"""
    offer = models.OneToOneField(Offer, verbose_name="Предложение", on_delete=models.CASCADE)
    first = models.ForeignKey(User, verbose_name="Первый участник", on_delete=models.CASCADE, related_name='chat_first_user')
    second = models.ForeignKey(User, verbose_name="Второй участник", on_delete=models.CASCADE, related_name='chat_second_user')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class ChatMessage(models.Model):
    """Сообщения чата"""
    room = models.ForeignKey(RoomChat, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name='Отправитель', on_delete=models.CASCADE)
    message = models.TextField("Сообщения")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

# Room
# - user1
# - user2
#
#
# Mess
# - mess
# - кто написал
# - какая комната
# - дата
