from datetime import datetime, time
import logging
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status

class RequestLoggingMiddleware:
    """
    Docstring for RequestLoggingMiddleware
        Middleware to log incoming requests with timestamps.
    """
    # This runs once the server starts
    def __init__(self, get_response):
        # store the get_response callable
        self.get_response = get_response
        # configure logging -  create a logger using the file name
        self.logger = logging.getLogger(__name__)

    # This runs for each request
    def __call__(self, request):
        # get the current user
        user = request.user

        #log the time, user and request path
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # call the next middleware or view
        response = self.get_response(request)

        return response

class RestrictAccessByTimeMiddleware:
    """
    This middleware restricts access to the application
    outside the allowed time window (6:00pm to 9:00pm)
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Runs for every incoming request
        checks the current time and restricts access if outside allowed hours
        """
        
        #Getting the current time
        current_time = timezone.now().time()

        if not (current_time > time(hour=18) and current_time < time(hour=21)):
            return JsonResponse(
                {
                    "error": "Chat is restricted at this time"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        
        #if within allowed time, proceed to the next middleware or view
        response = self.get_response(request)

        return response
    


        
