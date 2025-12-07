import hashlib
import json
from urllib import request as urllib_request, error as urllib_error
from django.utils.deprecation import MiddlewareMixin
from .models import VisitorTracking


class VisitorTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to automatically track visitor sessions and page views.
    Creates unique session identifiers based on IP address and user agent.
    Fetches geographic location data from IP address.
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
        
        # If visitor is new and has no location data, fetch it
        if created and not visitor.country:
            geo_data = self.get_geolocation(ip_address)
            if geo_data:
                visitor.country = geo_data.get('country', '')
                visitor.country_code = geo_data.get('countryCode', '')
                visitor.region = geo_data.get('regionName', '')
                visitor.city = geo_data.get('city', '')
                visitor.timezone = geo_data.get('timezone', '')
                visitor.latitude = geo_data.get('lat')
                visitor.longitude = geo_data.get('lon')
                visitor.save()
        
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
    
    def get_geolocation(self, ip_address):
        """
        Fetch geolocation data from IP address using ip-api.com
        Returns dict with location data or None if failed
        """
        # Skip geolocation for localhost/private IPs
        if ip_address in ['127.0.0.1', 'localhost'] or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
            return {
                'country': 'Local',
                'countryCode': 'LC',
                'regionName': 'Local',
                'city': 'Localhost',
                'timezone': 'UTC',
                'lat': 0.0,
                'lon': 0.0
            }
        
        try:
            # Free tier: http://ip-api.com/json/{ip}
            # Returns: country, countryCode, region, regionName, city, zip, lat, lon, timezone, etc.
            url = f"http://ip-api.com/json/{ip_address}?fields=status,country,countryCode,region,regionName,city,timezone,lat,lon"
            
            with urllib_request.urlopen(url, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get('status') == 'success':
                    return data
                
        except (urllib_error.URLError, urllib_error.HTTPError, json.JSONDecodeError, Exception):
            # Silently fail - don't block request if geolocation fails
            pass
        
        return None

