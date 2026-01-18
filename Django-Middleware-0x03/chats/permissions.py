from rest_framework import permissions
from chats.models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of a conversation.
    """

    def has_object_permission(self, request, view, obj):
        """
        Make sure only participants can PUT/GET/DELETE
        messages or conversations
        """
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # If the object is a Conversation
        if isinstance(obj, Conversation):
            return user in obj.participants.all()

        # If the object is a Message, check the conversation's participants
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False

    def has_permission(self, request, view):
        """
        Restrict sending messages to participants only.
        """
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        conversation_id = request.data.get("conversation") or view.kwargs.get("conversation_pk")
        if conversation_id:
            try:
                conversation = Conversation.objects.get(pk=conversation_id)
                return user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False
        return True