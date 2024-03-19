from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()

class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        participants = [self.request.user] + serializer.validated_data.get('participants')
        chat, _ = Chat.objects.get_or_create(participants=participants)
        serializer.save(participants=participants)

class ChatRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = Chat.objects.get(id=chat_id)
        serializer.save(chat=chat, sender=self.request.user)

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]