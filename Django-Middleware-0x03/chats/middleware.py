from datetime import datetime, time
import logging
from urllib import response
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
    
class OffensiveLanguageMiddleware:
    """
        This middleware tracks the number of chat messages sent by
        each ip address and implements a 5 message per limit
        timeline.
        """
    ips = {}

    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        response = self.get_response(request)

        return response    
       

class RolepermissionMiddleware:
    """
    Middleware to enforce role-based access control.

    - Checks the user's role from the request (assumes a 'role' field exists on the user model).
    - Only allows users with roles 'admin' or 'moderator'.
    - Returns a 403 Forbidden response if the user does not have permission.
    """

    # Allowed roles
    ALLOWED_ROLES = ['admin', 'moderator']

    def __init__(self, get_response):
        """
        Runs once when the server starts.
        Stores the next middleware or view function.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Runs for every incoming request.
        Checks user role and blocks access if unauthorized.
        """
        # Only check authenticated users
        user = request.user
        if not user.is_authenticated:
            return JsonResponse(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Check if user has a 'role' attribute
        user_role = getattr(user, 'role', None)
        if user_role not in self.ALLOWED_ROLES:
            # User is not allowed
            return JsonResponse(
                {'error': 'You do not have permission to access this resource.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Continue processing the request
        response = self.get_response(request)
        return response
        

        


        
