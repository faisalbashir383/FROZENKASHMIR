import hashlib
from django.utils.deprecation import MiddlewareMixin
from .models import VisitorTracking


class VisitorTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to automatically track visitor sessions and page views.
    Creates unique session identifiers based on IP address and user agent.
    """
    
    def process_request(self, request):
        """Track visitor on each request"""
        # Skip tracking for admin panel and static files
        if request.path.startswith('/admin') or request.path.startswith('/static'):
            return None
        
        # Get visitor information
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        referrer = request.META.get('HTTP_REFERER', '')[:500]
        
        # Create unique session key from IP and user agent
        session_key = self.generate_session_key(ip_address, user_agent)
        
        # Get or create visitor tracking record
        visitor, created = VisitorTracking.objects.get_or_create(
            session_key=session_key,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'referrer': referrer,
                'page_views': 1
            }
        )
        
        # If visitor already exists, increment page views
        if not created:
            visitor.page_views += 1
            visitor.save(update_fields=['page_views', 'last_visit'])
        
        # Attach visitor to request for potential use in views
        request.visitor = visitor
        
        return None
    
    def get_client_ip(self, request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def generate_session_key(self, ip_address, user_agent):
        """Generate unique session key from IP and user agent"""
        combined = f"{ip_address}:{user_agent}"
        return hashlib.sha256(combined.encode()).hexdigest()
