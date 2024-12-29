from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):  # For Conversation
            return request.user in obj.participants.all()
        if hasattr(obj, 'conversation'):  # For Message
            return request.user in obj.conversation.participants.all()
        return False
