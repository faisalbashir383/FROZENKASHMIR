from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Package, Destination


class PackageSitemap(Sitemap):
    """Sitemap for travel packages"""
    changefreq = "weekly"
    priority = 0.9
    
    def items(self):
        return Package.objects.all()
    
    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, obj):
        return reverse('package_detail', args=[obj.slug])


class DestinationSitemap(Sitemap):
    """Sitemap for destinations"""
    changefreq = "monthly"
    priority = 0.8
    
    def items(self):
        return Destination.objects.all()
    
    def location(self, obj):
        return reverse('destination_detail', args=[obj.slug])


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.7
    changefreq = "monthly"
    
    def items(self):
        return ['home', 'contact', 'package_list', 'destination_list']
    
    def location(self, item):
        return reverse(item)
