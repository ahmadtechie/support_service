import uuid
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from support_service.chats.models import Conversation


def generate_uuid():
    return uuid.uuid4()


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    def __init__(self, *args, **kwargs):
        customer_id = generate_uuid()
        admin_id = generate_uuid()

        super().__init__(args, kwargs)
        self.customer_id = customer_id
        self.admin_id = admin_id
        self.conversation = None
        self.conversation_id = None

    def connect(self):
        print("Connected!")
        self.customer = self.scope['customer']
        self.accept()

        self.conversation, created = Conversation.objects.get_or_create(
            customer_id=self.customer_id,
            admin_id=self.admin_id,
        )
        self.conversation_id = self.conversation.id

        async_to_sync(self.channel_layer.group_add)(
            self.conversation_id,
            self.channel_name,
        )

        self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey there! You've successfully connected!",
            }
        )

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "chat_message_echo",
                    "name": content["name"],
                    "message": content["message"],
                },
            )
        return super().receive_json(content, **kwargs)

    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)
