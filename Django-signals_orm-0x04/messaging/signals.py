from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from messaging.models import Message, Notification, MessageHistory, User


@receiver(post_save, sender=Message, dispatch_uid='create_notification')
def create_notification(sender, instance, created, **kwargs):
    """
    create a notification when a new message is sent
    """
    if created:
        Notification.objects.create(
            receiver=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message, dispatch_uid='update_message_history')
def create_message_history(sender, instance, **kwargs):
    """
    Add a message history record once a message is edited
    """
    if not instance.pk:
        return
    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if instance.content != old_instance.content:
        MessageHistory.objects.create(
            message=instance,
            content=instance.content,
            edited_by=instance.sender
        )
        instance.edited = True

@receiver(post_delete, sender=User, dispatch_uid='delete_user_information')
def delete_user_info(sender, instance, **kwargs):
    with transaction.atomic():
        Notification.objects.filter(receiver=instance).delete()
        Message.objects.filter(receiver=instance).delete()
        Message.objects.filter(sender=instance).delete()