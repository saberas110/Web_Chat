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
        print('user is ',user)
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
        user = self.scope['user']
        print('user is ', user)
        if user is None or user.is_anonymous:
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




    @database_sync_to_async
    def get_old_message(self, conversation_id):
        Conversation.objects.filter(participants__id = conversation_id)
        query = Message.objects.filter(conversation_id=conversation_id).order_by('created_at')
        return MessageSerializer(query, many=True, context={'user':self.scope['user']}).data

