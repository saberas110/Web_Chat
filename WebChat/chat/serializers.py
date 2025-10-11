from datetime import datetime

from django.db.models import Q
from django.template.context_processors import request
from django.utils import timezone
from rest_framework import serializers

from chat.models import Conversation, Message, Contact, UserProfile


class MessageSerializer(serializers.ModelSerializer):

    isMe = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['id', 'text', 'isMe', 'created_at']

    def get_isMe(self, obj):
        user = self.context.get('user')
        print('user is ',user)
        print('im from meSeri user is: ', obj.sender.id)
        if obj.sender == user:
            return True
        return False

    def get_created_at(self, obj):
        time = obj.created_at
        new_time = timezone.localtime(time)
        return new_time.strftime('%H:%M')



class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    contact_user = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'last_message', 'unread', 'avatar', 'contact_user']

    def _get_users(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        other_user = obj.participants.exclude(id=user.id).first() if user else None
        return user, other_user


    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-created_at').first()
        if last_message:
            return last_message.text
        return None

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

    def get_contact_user(self, obj):
        print('im from get contact_user', obj)
        _, other_user = self._get_users(obj)
        return other_user.id





class ContactsSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    last_seen = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'nickname', 'contact_user', 'avatar', 'last_seen', 'is_online']

    def _get_user(self,obj):
        request = self.context.get('request')
        user = request.user if request else None
        return user

    def get_avatar(self, obj):
        request = self.context.get('request')
        avatar = obj.contact_user.images.filter(is_main=True).first()
        if avatar and avatar.image:
            main_avatar = getattr(avatar, 'image', None)
            return request.build_absolute_uri(main_avatar.url)
        return None


    def get_last_seen(self, obj):
        user_profile = obj.contact_user.userprofile
        if user_profile and user_profile.last_seen:
            return user_profile.last_seen
        return None

    def get_is_online(self, obj):
        user_profile = obj.contact_user.userprofile
        if user_profile and user_profile.is_online:
            return user_profile.is_online
        return None
