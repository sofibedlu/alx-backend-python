from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create the base router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create the nested router
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]

