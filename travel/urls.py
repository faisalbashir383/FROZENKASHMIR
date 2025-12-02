from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.package_list, name='package_list'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
]
