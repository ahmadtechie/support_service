from django.contrib import admin
from .models import Conversation, Message


class ConversationModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('-created_at',)


class MessageModel(admin.ModelAdmin):
    list_display = ('conversation', 'from_user_email', 'to_user_email', 'content', 'timestamp', 'read')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('-timestamp',)


admin.site.register(Conversation, ConversationModel)
admin.site.register(Message, MessageModel)
