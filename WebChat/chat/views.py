from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Conversation
from chat.serializers import ConversationSerializer


class ConversationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        conversation = Conversation.objects.filter(participants=user)
        if not conversation.exists():
            return  Response({'message':'empty user conversation'})

        srz_data = ConversationSerializer(conversation, many=True, context={'request':request})
        return Response(srz_data.data, status=status.HTTP_200_OK)


