from django.contrib import admin

from .models import Property, Location, Appliance

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'zip_code', 'created_at', 'updated_at', 'activated')
    list_filter = ('created_at', 'updated_at', 'activated')
    search_fields = ('name', 'address', 'city', 'state', 'zip_code')
    ordering = ('name', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'created_at', 'updated_at', 'activated')
    list_filter = ('created_at', 'updated_at', 'activated')
    search_fields = ('name', 'property')
    ordering = ('name', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at', 'updated_at', 'activated')
    list_filter = ('created_at', 'updated_at', 'activated')
    search_fields = ('name', 'location')
    ordering = ('name', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')