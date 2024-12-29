from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'full_name', 'email', 'phone_number', 'role', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True, source='sender_id')

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
    
    def validate_message_body(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Message body cannot be empty')
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only=True, many=True)
    messages = MessageSerializer(read_only=True, many=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'participant_count']

    def get_participant_count(self, obj):
        return obj.participants.count()