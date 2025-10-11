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
        if not conversation.exists():
            return  Response({'message':'empty user conversation'})
        srz_data = ConversationSerializer(conversation, many=True, context={'request':request})
        print('srz i s :', srz_data.data)
        return Response(srz_data.data, status=status.HTTP_200_OK)



class ConversationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        other_user_id = request.data.get('id')
        conversation = (Conversation.objects.filter(participants__id=user.id)
                        .filter(participants__id=other_user_id).distinct().first())
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(user.id, other_user_id)
            conversation.save()
        return Response({'conversationId': conversation.id}, status.HTTP_200_OK)



class TestView(APIView):
    def get(self, request):
        cons = Contact.objects.filter(owner=request.user)
        for contact in cons:

            print(contact.contact_user.userprofile.last_seen)
        return Response({'message':'hello'})



class ContactsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        contacts = Contact.objects.filter(owner=user)
        if not contacts.exists():
            return Response({'message':{'شما هیچ مخاطبی ندارید'}})

        srz_data = ContactsSerializer(contacts, many=True, context={'request':request})
        return Response(srz_data.data, status.HTTP_200_OK)














