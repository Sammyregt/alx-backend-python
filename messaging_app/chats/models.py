from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
from datetime import datetime

# Create your models here.
class UserRole(models.TextChoices):
    GUEST = 'guest'
    HOST = 'host'
    ADMIN = 'admin'

class USER(AbstractUser):
    """
    user_id (Primary Key, UUID, Indexed)
    first_name (VARCHAR, NOT NULL)
    last_name (VARCHAR, NOT NULL)
    email (VARCHAR, UNIQUE, NOT NULL)
    password_hash (VARCHAR, NOT NULL)
    phone_number (VARCHAR, NULL)
    role (ENUM: 'guest', 'host', 'admin', NOT NULL)
    created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=False, unique=True, db_index=True)
    password_hash = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    role = models.CharField(choices=UserRole.choices, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    """
    conversation_id (Primary Key, UUID, Indexed)
    participants_id (Foreign Key, references User(user_id))
    created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    """
    conversation_id = models.UUIDField(primary_key=True, dafault=uuid.uuid4, editable=False)
    participants_id = models.ManyToManyField(USER, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    """
    message_id (Primary Key, UUID, Indexed)
    sender_id (Foreign Key, references User(user_id))
    message_body (TEXT, NOT NULL)
    sent_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(User, related_nam="message", on_delete=models.CASCADE)
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
