from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, MessageHistoryViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'message-history', MessageHistoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]