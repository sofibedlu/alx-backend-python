from rest_framework import serializers
from .models import Message, MessageHistory

class MessageHistorySerializer(serializers.ModelSerializer):
    edited_by = serializers.StringRelatedField()  # Display the username of the editor

    class Meta:
        model = MessageHistory
        fields = ['old_content', 'edit_timestamp', 'edited_by']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # Display the username of the sender
    receiver = serializers.StringRelatedField()  # Display the username of the receiver
    edited_by = serializers.StringRelatedField()  # Display the username of the editor
    history = MessageHistorySerializer(many=True, read_only=True)  # Include edit history

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'edited_at', 'edited_by', 'history']