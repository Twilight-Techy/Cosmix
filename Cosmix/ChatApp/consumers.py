import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'private_chat_{self.username}_{self.scope["user"].username}'

        # Add user to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Broadcast that the user is online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'status': 'online',
                'user': self.scope["user"].username
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Broadcast that the user is offline
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'status': 'offline',
                'user': self.scope["user"].username
            }
        )

        # Remove user from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope["user"].username,
                'picture_url': self.scope["user"].userprofile.picture.url,
                'timestamp': timezone.now().strftime('%H:%M')
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        picture_url = event['picture_url']
        timestamp = event['timestamp']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'picture_url': picture_url,
            'timestamp': timestamp,
        }))

    async def user_status(self, event):
        status = event['status']
        user = event['user']

        # Send the status update to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'user': user
        }))


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Add user to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Broadcast that the user is online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'status': 'online',
                'user': self.scope["user"].username
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Broadcast that the user is offline
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'status': 'offline',
                'user': self.scope["user"].username
            }
        )

        # Remove user from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def user_status(self, event):
        status = event['status']
        user = event['user']

        # Send the status update to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'user': user
        }))
