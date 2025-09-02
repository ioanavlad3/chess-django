# hello/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'
        print(f"Consumer connected: room={self.room_name}, group={self.room_group_name}, channel={self.channel_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f"Consumer disconnected: room={self.room_name}, code={close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Received data: {text_data}")
        data = json.loads(text_data)
        fen = data['fen']

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game.move',
                'fen': fen
            }
        )

    async def game_move(self, event):
        fen = event['fen']
        print(f"Broadcasting move: fen={fen}")
        await self.send(text_data=json.dumps({
            'fen': fen
        }))