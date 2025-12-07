from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    highlights = models.TextField(help_text="Comma separated highlights")
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name

class Package(models.Model):
    CATEGORY_CHOICES = [
        ('honeymoon', 'Honeymoon'),
        ('family', 'Family'),
        ('adventure', 'Adventure'),
        ('budget', 'Budget'),
        ('luxury', 'Luxury'),
        ('group', 'Group Tours'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('difficult', 'Difficult'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    duration = models.CharField(max_length=100, help_text="e.g. 3 Days / 2 Nights")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overview = models.TextField()
    itinerary = models.TextField(help_text="Detailed day-wise itinerary")
    inclusions = models.TextField()
    exclusions = models.TextField()
    image = models.ImageField(upload_to='packages/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New fields for filtering
    activities = models.TextField(blank=True, help_text="Comma-separated activities (e.g., skiing, trekking, sightseeing)")
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    group_size_min = models.PositiveIntegerField(default=1, help_text="Minimum group size")
    group_size_max = models.PositiveIntegerField(default=50, help_text="Maximum group size")
    popularity_score = models.IntegerField(default=0, help_text="Auto-calculated based on bookings and reviews")
    
    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0
    
    def update_popularity_score(self):
        """Update popularity score based on bookings and reviews"""
        booking_count = self.bookings.count()
        review_count = self.reviews.count()
        avg_rating = self.get_average_rating()
        
        # Simple popularity formula: bookings * 10 + reviews * 5 + avg_rating * 20
        self.popularity_score = (booking_count * 10) + (review_count * 5) + int(avg_rating * 20)
        self.save()
        return self.popularity_score
    
    def get_activities_list(self):
        """Return activities as a list"""
        if self.activities:
            return [activity.strip() for activity in self.activities.split(',')]
        return []


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    travel_date = models.DateField()
    travelers = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.package.title}"

class Inquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Inquiry from {self.name}"

class Review(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.rating} stars by {self.name}"

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text="City, Country")
    testimonial = models.TextField()
    avatar_url = models.URLField(default='https://randomuser.me/api/portraits/lego/1.jpg', help_text="URL to profile picture")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    is_featured = models.BooleanField(default=True, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100, default='FrozenKashmir Team')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    featured_image = models.URLField(help_text="URL to featured image from Unsplash")
    excerpt = models.TextField(max_length=300, help_text="Short summary for listings")
    content = models.TextField(help_text="Full blog post content")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    is_featured = models.BooleanField(default=False, help_text="Featured on homepage")
    view_count = models.PositiveIntegerField(default=0)
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def increment_views(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

class VisitorTracking(models.Model):
    """Track unique website visitors and their activity"""
    session_key = models.CharField(max_length=100, unique=True, help_text="Unique session identifier")
    ip_address = models.GenericIPAddressField(help_text="Visitor IP address")
    email = models.EmailField(blank=True, help_text="Visitor email address (if provided)")
    
    # Geographic information
    country = models.CharField(max_length=100, blank=True, help_text="Country name")
    country_code = models.CharField(max_length=2, blank=True, help_text="ISO country code")
    region = models.CharField(max_length=100, blank=True, help_text="State/Region/Province")
    city = models.CharField(max_length=100, blank=True, help_text="City name")
    timezone = models.CharField(max_length=50, blank=True, help_text="Timezone")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Longitude")
    
    user_agent = models.CharField(max_length=500, blank=True, help_text="Browser/device information")
    first_visit = models.DateTimeField(auto_now_add=True, help_text="First time visitor accessed site")
    last_visit = models.DateTimeField(auto_now=True, help_text="Most recent visit")
    page_views = models.PositiveIntegerField(default=1, help_text="Total pages viewed in this session")
    referrer = models.URLField(max_length=500, blank=True, help_text="Page that referred the visitor")
    
    class Meta:
        ordering = ['-last_visit']
        verbose_name = 'Visitor Tracking'
        verbose_name_plural = 'Visitor Tracking'
    
    def __str__(self):
        location = f"{self.city}, {self.country}" if self.city and self.country else self.ip_address
        return f"{location} - {self.page_views} views"
    
    @classmethod
    def get_unique_visitor_count(cls):
        """Get total count of unique visitors"""
        return cls.objects.count()
    
    @classmethod
    def get_total_page_views(cls):
        """Get total page views across all visitors"""
        from django.db.models import Sum
        result = cls.objects.aggregate(total_views=Sum('page_views'))
        return result['total_views'] or 0

class ContactSubmission(models.Model):
    """Store contact information submitted by visitors"""
    email = models.EmailField(blank=True, help_text="Visitor email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Visitor phone number")
    source_page = models.CharField(max_length=500, help_text="Page URL where contact was submitted")
    message = models.TextField(blank=True, help_text="Optional message from visitor")
    subscribed_newsletter = models.BooleanField(default=False, help_text="Opted in for newsletter")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
    
    def __str__(self):
        contact = self.email or self.phone or 'No contact'
        return f"{contact} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def clean(self):
        """Ensure at least email or phone is provided"""
        from django.core.exceptions import ValidationError
        if not self.email and not self.phone:
            raise ValidationError('At least one of email or phone must be provided.')
    
    def save(self, *args, **kwargs):
        """Run validation before saving"""
        self.clean()
        super().save(*args, **kwargs)
