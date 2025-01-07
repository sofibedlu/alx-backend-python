from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('created_at')
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username']
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        participants_emails = request.data.get('participants', [])
        if not isinstance(participants_emails, list):
            return Response({"error": "Participants field must be a list of emails."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch participants
        participants = list(User.objects.filter(email__in=participants_emails))
        
        # Add the current user
        if request.user not in participants:
            participants.append(request.user)

        # Serialize and validate data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create conversation and set participants
        conversation = serializer.save()  # Save the serializer to create the conversation
        conversation.participants.set(participants)  # Add participants

        # Serialize the created object for the response
        response_serializer = self.get_serializer(conversation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body']
    ordering_fields = ['sent_at']

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        data = request.data.copy()
        data['conversation'] = conversation_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender_id=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer