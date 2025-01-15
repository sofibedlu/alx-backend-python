import logging
from datetime import datetime

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