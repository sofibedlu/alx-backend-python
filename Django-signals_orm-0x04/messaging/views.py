from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from .models import Message, MessageHistory

def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-edit_timestamp')
    return render(request, 'message_history.html', {'message': message, 'history': history})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This triggers CASCADE deletions and signals
        logout(request)  # Log the user out after deletion
        return redirect('home')  # Redirect to a confirmation page
    return render(request, 'delete_user_confirmation.html')

def threaded_conversation(request, message_id):
    # Fetch the root message and all replies recursively
    root_message = Message.objects.select_related('sender', 'receiver').prefetch_related(
        'replies__sender',
        'replies__receiver',
    ).get(id=message_id)

    return render(request, 'threaded_conversation.html', {'root_message': root_message})

from django.db.models import Prefetch

def get_threaded_messages():
    # Prefetch replies recursively (up to a certain depth)
    return Message.objects.filter(parent_message__isnull=True).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        ))
    )