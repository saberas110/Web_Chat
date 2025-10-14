import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from chat.models import Message, Conversation
from chat.serializers import MessageSerializer
from chat.views import ConversationView


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user is None or user.is_anonymous:
            await self.close()
            return

        self.group_name = 'presence'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.set_online(user, True)


        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "presence.update",
                "user_id": user.id,
                "username": getattr(user, "username", None),
                "status": "online",
            }
        )

    async def disconnect(self, code):
        user = self.scope.get('user')
        if user is None or user.is_anonymous:
            return

        await self.set_last_seen(user)
        await self.set_online(user, False)
        await self.channel_layer.group_send(
            self.group_name, {
                "type": "presence.update",
                "user_id": user.id,
                "username": getattr(user, 'username', None),
                "status": "offline",
            }
        )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)




    async def presence_update(self, event):
        await self.send(text_data=json.dumps(event))



    @database_sync_to_async
    def set_online(self, user, val: bool):
        profile = getattr(user, "userprofile", None)
        if profile:
            profile.is_online = val
            profile.save(update_fields=['is_online', 'last_seen'])

    @database_sync_to_async
    def set_last_seen(self, user):
        profile = getattr(user, "userprofile", None)
        if profile:
            profile.last_seen = timezone.now()
            profile.save(update_fields=["last_seen", "is_online"])



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user is None or self.user.is_anonymous:
            await self.close(code=4001, reason='token_expired')
            return

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_chat_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(self.room_chat_name, self.channel_name)
        await self.accept()

        old_message = await self.get_old_message(self.conversation_id)

        await self.send(text_data=json.dumps({
            'type': 'init_message',
            'messages': old_message
        }))


    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "chat_message":
            message_text = data.get("messages")

            message = await self.create_message(self.user, self.conversation_id, message_text)
            serialized = MessageSerializer(message, context={'user': self.user}).data
            await self.channel_layer.group_send(self.room_chat_name, {
                "type": "chat.message",
                "message": serialized,
                "sender_id": self.user.id,
            })

    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        is_me = (self.user.id == sender_id)
        message["isMe"] = is_me
        await self.send(text_data=json.dumps({
            "type": "new_message",
            "message": event["message"]
        }))



    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_chat_name, self.channel_name)



    @database_sync_to_async
    def get_old_message(self, conversation_id):
        Conversation.objects.filter(participants__id = conversation_id)
        query = Message.objects.filter(conversation_id=conversation_id).order_by('created_at')
        return MessageSerializer(query, many=True, context={'user':self.scope['user']}).data

    @database_sync_to_async
    def create_message(self, user, conversation_id, text):
        message = Message.objects.create(sender=user, conversation_id=conversation_id, text=text)
        return message


