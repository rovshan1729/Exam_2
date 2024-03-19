from django.urls import path
from .views import ChatListCreateView, ChatRetrieveUpdateDestroyView, \
MessageListCreateView, MessageRetrieveUpdateDestroyView

urlpatterns= [
    path('chats/', ChatListCreateView.as_view()),
    path('chats/<int:pk>/', ChatRetrieveUpdateDestroyView.as_view()),
    path('chats/<int:chat_id>/messages/', MessageListCreateView.as_view()),
    path('chats/<int:chat_id>/messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view()),
]