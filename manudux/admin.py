from django.contrib import admin

from .models import Property, Location, Appliance, Part, Generator, Stock, StockItem

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

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'appliance', 'created_at', 'updated_at', 'activated')
    list_filter = ('created_at', 'updated_at', 'activated')
    search_fields = ('name', 'appliance')
    ordering = ('name', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Generator)
class GeneratorAdmin(admin.ModelAdmin):
    list_display = ('name', 'generator', 'created_at', 'updated_at', 'activated')
    list_filter = ('created_at', 'updated_at', 'activated')
    search_fields = ('name', 'generator')
    ordering = ('name', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at', 'updated_at', 'activated')
    list_filter = ('created_at', 'updated_at', 'activated')
    search_fields = ('name', 'location')
    ordering = ('name', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('stock', 'part', 'quantity', 'condition', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('stock', 'part', 'quantity', 'condition')
    ordering = ('stock', 'part', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')