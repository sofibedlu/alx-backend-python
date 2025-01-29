from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # New field to track edits

    def __str__(self):
        return f'From {self.sender} to {self.receiver} at {self.timestamp}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user} about message {self.message.id}'
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edit_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edit_timestamp}"