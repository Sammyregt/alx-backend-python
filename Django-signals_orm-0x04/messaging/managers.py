from django.db import models

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def unread_for_user(self, user):
        return self.get_queryset.filter(receiver=user, read=False)