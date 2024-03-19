from rest_framework import serializers
from .models import Message, Chat
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'created_at',
            'updated_at',
        )


class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = (
            'id', 
            'participants', 
            'created_at',
            'updated_at',
        )


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = (
            'id', 
            'sender',    
            'text', 
            'timestamp', 
            'is_read'
            'created_at',
            'updated_at',
        )
