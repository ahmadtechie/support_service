import uuid
from django.db import models


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.UUIDField()  # User ID of the customer
    admin_id = models.UUIDField(null=True, blank=True)  # User ID of the admin (if assigned)
    vendor_id = models.UUIDField(null=True, blank=True)  # User ID of the vendor (if assigned)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation-{self.id} with Customer-{self.customer_id}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    from_user_id = models.UUIDField()
    to_user_id = models.UUIDField()
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From User-{self.from_user_id} to User-{self.to_user_id}: {self.content} [{self.timestamp}]"
