from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True, related_name='locations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Appliance(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True, related_name='appliances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Appliance"
        verbose_name_plural = "Appliances"
        
class Part(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE, blank=True, null=True, related_name='parts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Part"
        verbose_name_plural = "Parts"

class Generator(Appliance):
    fuel = models.CharField(max_length=255, blank=True, null=True)
    kw = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Generator"
        verbose_name_plural = "Generators"

class Stock(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='stocks')
    quantity = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"