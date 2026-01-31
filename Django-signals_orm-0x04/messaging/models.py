from django.db import models
from django.contrib.auth.models import AbstractUser
from messaging.managers import UnreadMessagesManager
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, null=False, db_index=True)
    first_name = models. CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'user: {self.id}'
    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    content = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    unread = UnreadMessagesManager()

    def __str__(self):
        return f'Message {self.id} from {self.sender.id} to {self.receiver.id}'

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    receiver = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification {self.id} for {self.receiver.id}: {self.message.content}'


class MessageHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    message = models.ForeignKey(
        Message,
        related_name='message_history',
        on_delete=models.CASCADE)
    content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'MessageHistory {self.id} for message {self.message.id}: {self.content}'