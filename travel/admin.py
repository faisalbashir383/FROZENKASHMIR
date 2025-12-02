from django.contrib import admin
from .models import Destination, Package, Booking, Inquiry, Review, Testimonial

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
