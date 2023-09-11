
# # chat/consumers.py

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))



# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from asgiref.sync import async_to_sync


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
#         self.chat_group_name = f"chat_{self.chat_room_id}"

#         # Join room group
#         await self.channel_layer.group_add(
#             self.chat_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the room group
#         await self.channel_layer.group_discard(
#             self.chat_group_name,
#             self.channel_name
#         )

#     # async def receive(self, text_data):
#     #     # Process received message and send it back
#     #     await self.send(text_data=text_data)

#     # Receive message from WebSocket
#     # async def receive(self, text_data=None, bytes_data=None):

#     #     text_data_json = json.loads(text_data)
#     #     message = text_data_json['message']
#     #     # Send message to room group
#     #     await self.channel_layer.group_send(
#     #         self.chat_group_name,
#     #         {
#     #             'type': 'receive_group_message',
#     #             'message': message
#     #         }
#     #     )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))


#     async def chat_message(self, event):
#         message = event['message']
#         # Send message to WebSocket
#         await self.send(
#              text_data=json.dumps({
#             'message': message
#         }))
        
