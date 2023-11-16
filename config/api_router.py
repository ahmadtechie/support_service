from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from support_service.chats.api.views import ConversationRetrieveAPIView
from support_service.chats.api.views import MessageViewSet
from support_service.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register("messages", MessageViewSet)

urlpatterns = [
    path('chats/<uuid:user_id>/', ConversationRetrieveAPIView.as_view(), name='user.conversations'),
    path('chats/<uuid:user_id>/<conversation_name>', ConversationRetrieveAPIView.as_view(), name='user.conversations'),
]


app_name = "api"
urlpatterns += router.urls
