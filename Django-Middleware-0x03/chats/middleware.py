from datetime import datetime
import logging

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


        
