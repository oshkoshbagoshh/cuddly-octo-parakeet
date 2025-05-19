#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from django.core.cache import cache
from django.http import HttpResponseForbidden
import time

class RateLimitMiddleware:
    """
    Middleware to implement rate limiting for form submissions.
    
    This middleware checks if a user (identified by IP address) has exceeded
    the allowed number of requests within a specified time window.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Only apply rate limiting to POST requests to specific paths
        if request.method == 'POST' and self._should_rate_limit(request.path):
            client_ip = self._get_client_ip(request)
            
            # Create a cache key based on the IP and path
            cache_key = f"ratelimit:{client_ip}:{request.path}"
            
            # Get the current timestamp
            now = time.time()
            
            # Get the list of timestamps for this IP and path
            request_times = cache.get(cache_key, [])
            
            # Remove timestamps older than the time window (1 minute)
            time_window = 60  # 1 minute in seconds
            request_times = [t for t in request_times if now - t < time_window]
            
            # Check if the number of requests exceeds the limit
            max_requests = 5  # Maximum 5 requests per minute
            if len(request_times) >= max_requests:
                return HttpResponseForbidden("Too many requests. Please try again later.")
            
            # Add the current timestamp to the list
            request_times.append(now)
            
            # Store the updated list in the cache
            cache.set(cache_key, request_times, timeout=time_window)
        
        # Process the request normally
        return self.get_response(request)
    
    def _should_rate_limit(self, path):
        """
        Determine if the given path should be rate limited.
        
        Currently, we rate limit:
        - Contact form submissions
        - Signup form submissions
        - Any other form submissions
        """
        rate_limited_paths = [
            '/contact/',
            '/signup/',
            '/upload-ad-campaign/',
        ]
        
        return any(path.startswith(p) for p in rate_limited_paths)
    
    def _get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        
        This handles cases where the request is behind a proxy.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip