"""
URL configuration for frozenkashmir project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.http import FileResponse
from travel.sitemaps import PackageSitemap, DestinationSitemap, StaticViewSitemap, BlogPostSitemap
from travel.seo_views import robots_txt
import os


def serve_sw_js(request):
    """Serve the sw.js file for Monetag verification"""
    sw_path = os.path.join(settings.BASE_DIR, 'sw.js')
    return FileResponse(open(sw_path, 'rb'), content_type='application/javascript')


# Sitemap configuration
sitemaps = {
    'packages': PackageSitemap,
    'destinations': DestinationSitemap,
    'static': StaticViewSitemap,
    'blog': BlogPostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sw.js', serve_sw_js, name='service_worker'),  # Monetag verification
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include('travel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
