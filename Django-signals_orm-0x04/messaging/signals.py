from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.utils import timezone


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.id:  # Check if the message already exists (i.e., it's being edited)
        try:
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:  # Check if the content has changed
                # Log the old content in MessageHistory
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.edited_by  # Track who made the edit
                )
                # Mark the message as edited
                instance.edited = True
                instance.edited_at = timezone.now()
        except Message.DoesNotExist:
            pass  # Message is being created, not edited