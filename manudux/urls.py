

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('properties/', views.properties, name='properties'),
    path('properties/create-property/', views.create_property, name='create-property'),
    path('property/<int:pk>/', views.property_detail, name='property'),
    path('locations/create-location/', views.create_location, name='create-location'),
    path('locations/', views.locations, name='locations'),
    path('location/<int:pk>/', views.location_detail, name='location'),
    path('parts/', views.parts, name='parts'),
    path('part/<int:pk>/', views.part_detail, name='part'),
    path('appliances/', views.appliances, name='appliances'),
    path('appliance/<int:pk>/', views.appliance_detail, name='appliance'),
]