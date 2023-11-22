import json
import uuid
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from support_service.chats.models import Conversation, Message
from support_service.chats.api.serializers import MessageSerializer


def generate_uuid():
    return uuid.uuid4()


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)

    def __init__(self, *args, **kwargs):
        customer_id = generate_uuid()
        admin_id = generate_uuid()

        super().__init__(args, kwargs)
        self.customer_id = customer_id
        self.admin_id = admin_id
        self.conversation = None
        self.conversation_name = None

    def connect(self):
        print("Connected!")
        self.accept()

        self.conversation_name = f"{self.scope['url_route']['kwargs']['conversation_name']}"
        print('conversation_name ', self.conversation_name)
        self.conversation, created = Conversation.objects.get_or_create(
            name=self.conversation_name,
        )

        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        messages = self.conversation.messages.all().order_by("-timestamp")[0:50]
        self.send_json({
            "type": "last_50_messages",
            "customer_id": self.customer_id,
            "admin_id": self.admin_id,
            "messages": MessageSerializer(messages, many=True).data,
        })

    def disconnect(self, code):
        print("Disconnected!")
        # Ensure proper cleanup for disconnected client
        if hasattr(self, 'conversation_name') and self.conversation_name:
            # Remove the client from the conversation's channel group
            async_to_sync(self.channel_layer.group_discard)(
                self.conversation_name,
                self.channel_name,
            )

        # Call the parent disconnect method for default handling
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):
        try:
            message_type = content.get("type")

            if message_type == "any":
                print(content)

            if message_type == "start_conversation":
                print(content.get('data'))

            if message_type == "chat_message":
                from_user_id = content.get("from_user_id")
                to_user_id = content.get("to_user_id")
                message_content = content.get("message")

                # Create a new message and save it to the database
                message = Message.objects.create(
                    conversation=self.conversation,
                    from_user_id=from_user_id,
                    to_user_id=to_user_id,
                    content=message_content,
                )

                # Broadcast the message to everyone in the conversation group
                async_to_sync(self.channel_layer.group_send)(
                    self.conversation_name,
                    {
                        "type": "chat_message_echo",
                        "message": MessageSerializer(message).data,
                    },
                )
        except Exception as e:
            # Log or handle unexpected requests/errors
            print(f"Unexpected request: {content}")
            self.send_json({"error": "Unexpected request received"})

    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)
