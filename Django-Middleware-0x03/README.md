# Messaging App

This is a messaging application built with Django and Django REST Framework. It supports user authentication, conversation management, and message handling.

## Features

- User authentication with JWT
- Create and manage conversations
- Send and receive messages
- Filter and search messages


## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd messaging_app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

## API Endpoints

### Authentication

- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

### Conversations

- `GET /api/conversations/`: List all conversations
- `POST /api/conversations/`: Create a new conversation

### Messages

- `GET /api/conversations/{conversation_id}/messages/`: List all messages in a conversation
- `POST /api/conversations/{conversation_id}/messages/`: Send a new message in a conversation
