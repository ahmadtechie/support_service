from django.db.models import Q

from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


from .serializers import MessageSerializer
from .serializers import ConversationSerializer

from support_service.chats.models import Message
from support_service.chats.models import Conversation


class ConversationRetrieveAPIView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()

    def get_queryset(self):
        queryset = Conversation.objects.filter(
            Q(messages__from_user_id=self.kwargs['user_id']) |
            Q(messages__to_user_id=self.kwargs['user_id'])
        )
        return queryset


class MessageViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.none()

    def get_queryset(self):
        conversation_name = self.kwargs["conversation_name"]

        queryset = Message.objects.filter(
            Q(from_user_id=self.kwargs['user_id']) |
            Q(to_user_id=self.kwargs['user_id']) |
            Q(conversation__name__contains=conversation_name)
        ).order_by("-timestamp")
        return queryset
