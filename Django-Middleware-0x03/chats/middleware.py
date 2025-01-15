import logging
from datetime import datetime, time
from django.utils import timezone
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(asctime)s - User: %(user)s - Path: %(path)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def __call__(self, request):
        user = request.user.email if request.user.is_authenticated else 'Anonymous'
        path = request.path
        logging.info('', extra={'user': user, 'path': path})
        response = self.get_response(request)
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