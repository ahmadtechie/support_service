from rest_framework import serializers

from support_service.chats.models import Message, Conversation


class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "from_user_id",
            "to_user_id",
            "content",
            "timestamp",
            "read",
        )

    def get_conversation(self, obj):
        return str(obj.conversation.id)


class ConversationSerializer(serializers.ModelSerializer):
    # other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "name", "last_message")

    def get_last_message(self, obj):
        messages = obj.messages.all().order_by("-timestamp")
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data


