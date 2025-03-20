from django.db import models


class Property(models.Model):
    """Represents a property that can contain multiple locations."""
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
    """Represents a specific location within a property (e.g., garage, closet)."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='locations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.property.name} - {self.name}"

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Appliance(models.Model):
    """Represents an appliance within a location."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='appliances'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Appliance"
        verbose_name_plural = "Appliances"


class Generator(Appliance):
    """A specialized type of Appliance with additional fields."""
    fuel = models.CharField(max_length=255, blank=True, null=True)
    kw = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = "Generator"
        verbose_name_plural = "Generators"


class Part(models.Model):
    """Represents a part that belongs to an appliance."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    appliance = models.ForeignKey(
        Appliance, on_delete=models.CASCADE, related_name='parts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (for {self.appliance.name})"

    class Meta:
        verbose_name = "Part"
        verbose_name_plural = "Parts"


class Stock(models.Model):
    """Represents a stock location where parts are stored."""
    name = models.CharField(max_length=255)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='stocks', blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    def __str__(self):
        try:
            return f"{self.name} at {self.location.name}"
        except:
            return self.name

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class StockItem(models.Model):
    """Links a part to a specific stock location, tracking quantity and condition."""
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name='stock_items'
    )
    part = models.ForeignKey(
        Part, on_delete=models.CASCADE, related_name='stock_items'
    )
    quantity = models.PositiveIntegerField(default=0)
    condition = models.CharField(
        max_length=50, blank=True, null=True, help_text="e.g., New, Used, Broken"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.part.name} ({self.condition or 'Unknown'}) in {self.stock.name}"

    class Meta:
        verbose_name = "Stock Item"
        verbose_name_plural = "Stock Items"
