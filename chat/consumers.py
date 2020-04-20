import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import (WebsocketConsumer,
                                        AsyncWebsocketConsumer,
                                        JsonWebsocketConsumer,
                                        AsyncJsonWebsocketConsumer)
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

from chat.models import ChatMessage


class ChatConsumer(WebsocketConsumer):
    """Синхронный консьюмер"""
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user']

        ChatMessage.objects.create(room_id=self.room_name, user_id=user_id, message=message)
        # print(self.room_name)

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': user_id
            }
        )

    def chat_message(self, event):
        message = event['message']
        user_id = event['user']
        print(message)
        self.send(text_data=json.dumps({
            'event': "Send",
            'message': message,
            'user': user_id
        }))

        # for h in self.scope['headers']:
        #     print("HEADER", h[0], " >> ", h[1])
        #     print("***************************")
        # print("***************************")
        # print("URL_ROUTE", self.scope['url_route'])
        # print("***************************")
        # print("PATH", self.scope['path'])
        # json_data = json.loads(text_data)
        # message = json_data['message']
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))


class AsyncChatConsumer(AsyncWebsocketConsumer):
    """Асинхронный консьюмер"""
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_add(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message',
                'text': text_data,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=event['text'])


class BaseSyncConsumer(SyncConsumer):
    """Базовый синхронный консьюмер"""
    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": event['text']
        })


class BaseAsyncConsumer(AsyncConsumer):
    """Базовый асинхронный консьюмер"""
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })


class ChatJsonConsumer(JsonWebsocketConsumer):
    """Синхронный json консьюмер"""
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive_json(self, content, **kwargs):
        self.send_json(content=content)

    @classmethod
    def encode_json(cls, content):
        return super().encode_json(content)

    @classmethod
    def decode_json(cls, text_data):
        return super().decode_json(text_data)


class ChatAsyncJsonConsumer(AsyncJsonWebsocketConsumer):
    """Асинхронный json консьюмер"""
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive_json(self, content, **kwargs):
        await self.send_json(content=content)

    @classmethod
    async def encode_json(cls, content):
        return await super().encode_json(content)

    @classmethod
    async def decode_json(cls, text_data):
        return await super().decode_json(text_data)