from django.db.models import Q
from django.template.context_processors import request
from rest_framework import serializers

from chat.models import Conversation, Message, Contact

user =   {
    id: 1,
    'name': "Ali",
    'lastMessage': "درود، حالت چطوره؟",
    'time': "Sep 24",
    'unread': 2,
    'avatar': "https://i.pravatar.cc/40?img=1",
  },

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'last_message', 'unread', 'avatar']

    def _get_users(self, obj):
        if not hasattr(self, '_cached_user'):
            request = self.context.get('request')
            user = request.user if request else None
            other_user = obj.participants.exclude(id=user.id).first() if user else None
            self._cached_user = (user, other_user)
        return self._cached_user


    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-created_at').first().text
        return last_message

    def get_name(self, obj):
        user, other_user = self._get_users(obj)
        try:
            other_user_contact = Contact.objects.get(contact_user=other_user)
            return other_user_contact.nickname
        except Contact.DoesNotExist:
            return other_user.phone_number if other_user else None

    def get_avatar(self, obj):
        request = self.context.get('request')
        user, other_user = self._get_users(obj)
        avatar = other_user.images.filter(is_main=True).first()

        if avatar and avatar.image :
            main_avatar = getattr(avatar, 'image', None)
            return request.build_absolute_uri(main_avatar.url)
        return None

    def get_unread(self, obj):
        user, _ = self._get_users(obj)
        unread_count = obj.messages.exclude(sender=user).filter(
            ~Q(read_messages__user=user)
        ).count()
        return unread_count
