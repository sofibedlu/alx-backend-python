import logging
from datetime import datetime, time
from django.utils import timezone
from django.http import HttpResponseForbidden
from collections import defaultdict
import re
#from rest_framework_simplejwt.authentication import JWTAuthentication
#from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure a separate logger for request logging
        self.logger = logging.getLogger('request_logger')
        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(asctime)s - User: %(user)s - Path: %(path)s', '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user.email if request.user.is_authenticated else 'Anonymous'
        path = request.path
        logging.info('', extra={'user': user, 'path': path})
        response = self.get_response(request)

        # Modify the response by adding a custom header
        response['X-Processed-By'] = 'RequestLoggingMiddleware'

        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed access hours
        self.start_time = time(6, 0)  # 6:00 AM
        self.end_time = time(21, 0)   # 9:00 PM

    def __call__(self, request):
        if request.path.startswith('/api/conversations'):
            current_time = timezone.now().time()
            if not (self.start_time <= current_time <= self.end_time):
                return HttpResponseForbidden("Access to the chat is restricted at this time.")
        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track message counts per IP
        self.ip_message_counts = defaultdict(list)
        # Define the time window and maximum allowed messages
        self.TIME_WINDOW = 60  # seconds
        self.MAX_MESSAGES = 5

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/conversations/'):
            # Get the client's IP address
            ip_address = self.get_client_ip(request)
            current_time = timezone.now().timestamp()

            # Remove timestamps outside the time window
            message_times = self.ip_message_counts[ip_address]
            self.ip_message_counts[ip_address] = [
                timestamp for timestamp in message_times
                if current_time - timestamp < self.TIME_WINDOW
            ]

            if len(self.ip_message_counts[ip_address]) >= self.MAX_MESSAGES:
                return HttpResponseForbidden("Too many messages sent. Please try again later.")

            # Add the current timestamp
            self.ip_message_counts[ip_address].append(current_time)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Retrieve the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define paths using regular expressions and their allowed roles
        self.protected_paths = {
            r'^/api/conversations/$': ['admin'],  # Only admin can access the list of conversations
        }

        # Initialize JWT Authentication this is for testing perposes because in jwt auth is handled after the middleware
        #self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        # Manually authenticate the user, this is for testing perposes because in jwt auth is handled after the middleware
        # authentication should be handled someware else other than middleware or use permission classes
        """
        try:
            # This will return a tuple of (user, validated token)
            user_auth_tuple = self.jwt_authenticator.authenticate(request)
            if user_auth_tuple:
                request.user, _ = user_auth_tuple
        except (InvalidToken, AuthenticationFailed) as e:
            # If token is invalid, leave user as AnonymousUser
            pass
        """

        path = request.path
        user = request.user

        for path_pattern, roles in self.protected_paths.items():
            if re.match(path_pattern, path):
                if not user.is_authenticated:
                    return HttpResponseForbidden("You must be logged in to access this resource.")
                if not hasattr(user, 'role') or user.role not in roles:
                    return HttpResponseForbidden("You do not have permission to perform this action.")
                break

        response = self.get_response(request)
        return response