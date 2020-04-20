from django.contrib import admin

from .models import RoomChat, ChatMessage


class ChatMessageAdmin(admin.TabularInline):
    model = ChatMessage


class RoomAdmin(admin.ModelAdmin):
    inlines = [ChatMessageAdmin]

    class Meta:
        model = RoomChat


admin.site.register(RoomChat, RoomAdmin)
