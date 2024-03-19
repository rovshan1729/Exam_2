from django.db import models
from utils.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()



class Chat(BaseModel):
    participants = models.ManyToManyField(User, related_name='chats')


class Message(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')

    text = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    is_read = models.BooleanField(default=False, editable=False)

    upload_file = models.FileField(upload_to='media/message/', null=True, blank=True)


class Reaction(BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')

    reaction_type = models.CharField(max_length=16)




