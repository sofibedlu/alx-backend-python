from django.urls import path
from .views import message_history, delete_user

urlpatterns = [
    path('message/<int:message_id>/history/', message_history, name='message_history'),
    path('delete-user/', delete_user, name='delete_user'),
]
