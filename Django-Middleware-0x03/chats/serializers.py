from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model
    """
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender_id',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model
    """
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages'
        ]
        read_only_fields = ['conversation_id', 'created_at']

        def create(self, validated_data):
            participants = validated_data.pop('participants', [])
            conversation = Conversation.objects.create(**validated_data)

            # Add participants to the conversation
            if participants:
                conversation.participants.add(*participants)
            
            # Add Current user automatically
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                conversation.participants.add(request.user)
            return conversation
