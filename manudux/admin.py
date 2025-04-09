from django.contrib import admin
from django.core.files.storage import default_storage
import os
from manudux.models.guide_model import Guide
from manudux.models.property_model import Property
from manudux.models.guidefile_model import GuideFile
from manudux.models.guidestep_model import GuideStep
from manudux.models.location_model import Location
from manudux.models.property_type_model import PropertyType
from django.conf import settings
from django import forms
from django.urls import path, reverse
from django.shortcuts import redirect


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "city",
        "state",
        "zip_code",
        "created_at",
        "updated_at",
        "activated",
    )
    list_filter = ("created_at", "updated_at", "activated")
    search_fields = ("name", "address", "city", "state", "zip_code")
    ordering = ("name", "created_at", "updated_at")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    inlines = [LocationInline]

    change_list_template = "admin/property_changelist.html"  # Custom admin template

    def delete_unused_images_from_storage(self, request):
        """Deletes images that are no longer associated with any Property instance."""
        used_images = set(
            Property.objects.exclude(image="").values_list("image", flat=True)
        )

        media_path = os.path.join(
            settings.MEDIA_ROOT, "properties"
        )  # Adjust for your upload path
        if not os.path.exists(media_path):
            self.message_user(request, "No media folder found.", level="warning")
            return redirect(request.path)

        all_images = set(default_storage.listdir(media_path)[1])

        # Find images that are not used in the database
        unused_images = all_images - {os.path.basename(img) for img in used_images}

        # Delete unused images
        deleted_count = 0
        for image in unused_images:
            image_path = os.path.join(media_path, image)
            if default_storage.exists(image_path):
                default_storage.delete(image_path)
                deleted_count += 1

        self.message_user(
            request, f"Deleted {deleted_count} unused images from storage."
        )
        return redirect(reverse("admin:manudux_property_changelist"))

    def get_urls(self):
        """Adds a custom admin URL for triggering garbage collection."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "delete-unused-images/",
                self.admin_site.admin_view(self.delete_unused_images_from_storage),
                name="delete_unused_images",
            ),
        ]
        return custom_urls + urls


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "property", "created_at", "updated_at", "activated")
    list_filter = ("created_at", "updated_at", "activated")
    search_fields = ("name", "property")
    ordering = ("name", "created_at", "updated_at")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")


# @admin.register(Appliance)
# class ApplianceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'location', 'created_at', 'updated_at', 'activated')
#     list_filter = ('created_at', 'updated_at', 'activated')
#     search_fields = ('name', 'location')
#     ordering = ('name', 'created_at', 'updated_at')
#     date_hierarchy = 'created_at'
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(Part)
# class PartAdmin(admin.ModelAdmin):
#     list_display = ('name', 'appliance', 'created_at', 'updated_at', 'activated')
#     list_filter = ('created_at', 'updated_at', 'activated')
#     search_fields = ('name', 'appliance')
#     ordering = ('name', 'created_at', 'updated_at')
#     date_hierarchy = 'created_at'
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(Generator)
# class GeneratorAdmin(admin.ModelAdmin):
#     list_display = ('name', 'generator', 'created_at', 'updated_at', 'activated')
#     list_filter = ('created_at', 'updated_at', 'activated')
#     search_fields = ('name', 'generator')
#     ordering = ('name', 'created_at', 'updated_at')
#     date_hierarchy = 'created_at'
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(Stock)
# class StockAdmin(admin.ModelAdmin):
#     list_display = ('name', 'location', 'created_at', 'updated_at', 'activated')
#     list_filter = ('created_at', 'updated_at', 'activated')
#     search_fields = ('name', 'location')
#     ordering = ('name', 'created_at', 'updated_at')
#     date_hierarchy = 'created_at'
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(StockItem)
# class StockItemAdmin(admin.ModelAdmin):
#     list_display = ('stock', 'part', 'quantity', 'condition', 'created_at', 'updated_at')
#     list_filter = ('created_at', 'updated_at')
#     search_fields = ('stock', 'part', 'quantity', 'condition')
#     ordering = ('stock', 'part', 'created_at', 'updated_at')
#     date_hierarchy = 'created_at'
#     readonly_fields = ('created_at', 'updated_at')


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)


class GuideFileAdmin(admin.StackedInline):
    model = GuideFile
    extra = 1


class GuideStepInline(admin.TabularInline):
    model = GuideStep
    extra = 1  # This defines how many empty rows are shown by default
    fields = (
        "step_number",
        "title",
        "description",
        "image",
        "video",
    )  # You can adjust the fields as needed
    ordering = ("step_number",)


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "qr_code", "created_at", "updated_at")
    search_fields = ("name", "created_at", "updated_at")
    inlines = [GuideStepInline, GuideFileAdmin]  # PropertyInline, LocationInline


@admin.register(GuideFile)
class GuideFileAdmin(admin.ModelAdmin):
    pass


@admin.register(GuideStep)
class GuideStepAdmin(admin.ModelAdmin):
    list_display = ("guide", "step_number", "title", "created_at", "updated_at")
    list_filter = ("guide", "step_number")  # Optional filter by guide or step number
    search_fields = (
        "guide__name",
        "title",
        "description",
    )  # Allows searching by guide name, title, and description
