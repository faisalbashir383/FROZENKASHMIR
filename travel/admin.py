from django.contrib import admin
from .models import Destination, Package, Booking, Inquiry, Review, Testimonial, BlogCategory, BlogPost, VisitorTracking, ContactSubmission

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'best_time_to_visit')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'category', 'price', 'is_featured')
    list_filter = ('category', 'destination', 'is_featured')
    search_fields = ('title', 'destination__name')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'package', 'travel_date', 'status', 'created_at')
    list_filter = ('status', 'travel_date')
    search_fields = ('name', 'email', 'phone')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'package', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'name', 'rating', 'created_at')
    list_filter = ('rating',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'rating')
    search_fields = ('name', 'location', 'testimonial')

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'view_count', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('view_count', 'created_at', 'updated_at')

@admin.register(VisitorTracking)
class VisitorTrackingAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'email', 'get_location', 'timezone', 'first_visit', 'last_visit', 'page_views', 'get_browser')
    list_filter = ('country', 'first_visit', 'last_visit')
    search_fields = ('ip_address', 'email', 'city', 'country', 'session_key')
    readonly_fields = ('session_key', 'ip_address', 'email', 'country', 'country_code', 'region', 'city', 'timezone', 'latitude', 'longitude', 'user_agent', 'first_visit', 'last_visit', 'page_views', 'referrer')
    date_hierarchy = 'first_visit'
    
    def get_location(self, obj):
        """Display formatted location"""
        parts = []
        if obj.city:
            parts.append(obj.city)
        if obj.region:
            parts.append(obj.region)
        if obj.country:
            parts.append(obj.country)
        return ', '.join(parts) if parts else 'Unknown'
    get_location.short_description = 'Location'
    
    def get_browser(self, obj):
        """Extract browser name from user agent"""
        ua = obj.user_agent.lower()
        if 'chrome' in ua:
            return 'Chrome'
        elif 'firefox' in ua:
            return 'Firefox'
        elif 'safari' in ua:
            return 'Safari'
        elif 'edge' in ua:
            return 'Edge'
        return 'Other'
    get_browser.short_description = 'Browser'
    
    def has_add_permission(self, request):
        """Prevent manual addition of visitor records"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion for cleanup"""
        return True

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('get_contact', 'source_page_short', 'subscribed_newsletter', 'created_at')
    list_filter = ('subscribed_newsletter', 'created_at')
    search_fields = ('email', 'phone', 'message')
    readonly_fields = ('email', 'phone', 'source_page', 'message', 'subscribed_newsletter', 'created_at')
    date_hierarchy = 'created_at'
    
    def get_contact(self, obj):
        """Display email or phone"""
        if obj.email and obj.phone:
            return f"{obj.email} / {obj.phone}"
        return obj.email or obj.phone
    get_contact.short_description = 'Contact Info'
    
    def source_page_short(self, obj):
        """Display shortened source page URL"""
        if len(obj.source_page) > 50:
            return obj.source_page[:50] + '...'
        return obj.source_page
    source_page_short.short_description = 'Source Page'
    
    def has_add_permission(self, request):
        """Prevent manual addition"""
        return False

