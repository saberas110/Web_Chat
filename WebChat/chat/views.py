from django.db.models import Count
from redis.commands.search.reducers import count
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from chat.models import Conversation, Contact
from chat.serializers import ConversationSerializer, ContactsSerializer


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        conversation = Conversation.objects.filter(participants=user)
        print(conversation)
        if not conversation.exists():
            return  Response({'message':'empty user conversation'}, status.HTTP_404_NOT_FOUND)
        srz_data = ConversationSerializer(conversation, many=True, context={'request':request})
        return Response(srz_data.data, status=status.HTTP_200_OK)



class ConversationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        other_user_id = request.data.get('id')
        conversation = Conversation.objects.filter(participants__in=[user.id, other_user_id]).distinct()
        if not conversation:
            conversation = Conversation()
            conversation.save()
            conversation.participants.add(user.id, other_user_id)

            print("✅ Conversation created:", conversation.id)
        else:
            print("🔁 Existing conversation found:", conversation.id)
        return Response({'conversationId': conversation.id}, status.HTTP_200_OK)



class TestView(APIView):
    def get(self, request):
        cons = Contact.objects.filter(owner=request.user)
        return Response({'message':'hello'})



class ContactsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        contacts = Contact.objects.filter(owner=user)
        if not contacts.exists():
            return Response({'message':'شما هیچ مخاطبی ندارید'}, status.HTTP_404_NOT_FOUND)

        srz_data = ContactsSerializer(contacts, many=True, context={'request':request})
        return Response(srz_data.data, status.HTTP_200_OK)














