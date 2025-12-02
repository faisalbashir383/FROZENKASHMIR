from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Destination, Package, Booking, Inquiry, Review, Testimonial
import json
from urllib import request as urllib_request, parse as urllib_parse

def home(request):
    featured_packages = Package.objects.filter(is_featured=True)[:6]
    destinations = Destination.objects.all()  # Get all destinations for slider
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    return render(request, 'travel/home.html', {
        'featured_packages': featured_packages,
        'destinations': destinations,
        'testimonials': testimonials
    })

def get_recommended_packages(packages, user_preferences=None):
    """
    Get recommended packages based on popularity and user preferences.
    Simple recommendation algorithm.
    """
    # Start with featured packages
    recommended = list(packages.filter(is_featured=True))
    
    # Add popular packages (top 3 by popularity score)
    popular = list(packages.order_by('-popularity_score')[:3])
    for p in popular:
        if p not in recommended:
            recommended.append(p)
            
    # If we had user preferences, we would weight them here
    # For now, just return top 5 unique recommendations
    return recommended[:5]

def package_list(request):
    packages = Package.objects.all()
    
    # Filter by Category
    category = request.GET.get('category')
    if category:
        packages = packages.filter(category=category)
        
    # Filter by Price Range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        packages = packages.filter(price__gte=min_price)
    if max_price:
        packages = packages.filter(price__lte=max_price)
        
    # Filter by Difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        packages = packages.filter(difficulty_level=difficulty)
        
    # Filter by Activities (comma separated)
    activities = request.GET.get('activities')
    if activities:
        activity_list = activities.split(',')
        # Filter packages that contain ANY of the selected activities
        # This is a simple text search, ideally use Taggit or similar
        query = Q()
        for activity in activity_list:
            query |= Q(activities__icontains=activity.strip())
        packages = packages.filter(query)

    # Sorting
    sort_by = request.GET.get('sort', 'popularity') # Default to popularity
    if sort_by == 'price_low':
        packages = packages.order_by('price')
    elif sort_by == 'price_high':
        packages = packages.order_by('-price')
    elif sort_by == 'duration':
        packages = packages.order_by('duration') # Note: String sort might be imperfect for "5 Days" vs "10 Days"
    elif sort_by == 'rating':
        # optimizing for now by just using popularity score which includes rating
        packages = packages.order_by('-popularity_score')
    else: # popularity
        packages = packages.order_by('-popularity_score')

    # Get recommendations (from the filtered set or all packages if filtered set is small)
    recommendations = get_recommended_packages(Package.objects.all())

    context = {
        'packages': packages,
        'recommendations': recommendations,
        'categories': Package.CATEGORY_CHOICES,
        'difficulties': Package.DIFFICULTY_CHOICES,
    }
    return render(request, 'travel/package_list.html', context)

def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug)
    if request.method == 'POST':
        # Simple booking handling
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        travelers = request.POST.get('travelers')
        
        Booking.objects.create(
            package=package,
            name=name,
            email=email,
            phone=phone,
            travel_date=date,
            travelers=travelers
        )
        messages.success(request, 'Booking request submitted successfully!')
        return redirect('package_detail', slug=slug)
        
    return render(request, 'travel/package_detail.html', {'package': package})

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'travel/destination_list.html', {'destinations': destinations})


def _fetch_unsplash_gallery_images(query, count=4):
    """
    Fetch a small set of random images from the Unsplash API for the gallery.
    Uses the random photo endpoint:
    https://api.unsplash.com/photos/random?query=nature, &client_id=ldCBwwXw7Y4HM52es_bfQlhCNS1G_fXokFaf-CZiStE
    """
    base_url = "https://api.unsplash.com/photos/random"
    params = {
        "query": query or "nature",
        "count": count,
        "client_id": "ldCBwwXw7Y4HM52es_bfQlhCNS1G_fXokFaf-CZiStE",
    }
    url = f"{base_url}?{urllib_parse.urlencode(params)}"

    try:
        with urllib_request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return []

    # Unsplash returns a list when count > 1, otherwise a dict
    if isinstance(data, dict):
        data = [data]

    image_urls = []
    for item in data:
        urls = item.get("urls") or {}
        image_url = urls.get("regular") or urls.get("full") or urls.get("small")
        if image_url:
            image_urls.append(image_url)

    return image_urls


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    gallery_images = _fetch_unsplash_gallery_images(destination.name)
    return render(request, 'travel/destination_detail.html', {
        'destination': destination,
        'gallery_images': gallery_images
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        Inquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, 'Inquiry sent successfully!')
        return redirect('contact')
    return render(request, 'travel/contact.html')

def search(request):
    query = request.GET.get('destination', '')
    date = request.GET.get('date', '')
    travelers = request.GET.get('travelers', '')
    
    packages = Package.objects.all()
    
    if query:
        packages = packages.filter(
            Q(destination__name__icontains=query) | 
            Q(title__icontains=query)
        )
    
    return render(request, 'travel/search_results.html', {
        'packages': packages,
        'query': query,
        'date': date,
        'travelers': travelers
    })
