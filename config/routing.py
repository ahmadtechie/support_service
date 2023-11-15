from django.urls import path

from support_service.chats.consumers import ChatConsumer


websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi())
]
