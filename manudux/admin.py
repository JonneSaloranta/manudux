import os

from django.conf import settings
from django.contrib import admin
from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.urls import path, reverse

from manudux.models.appliance_model import Appliance
from manudux.models.appliancedocument_model import ApplianceDocument
from manudux.models.appliancetype_model import ApplianceType
from manudux.models.guide_model import Guide
from manudux.models.guidefile_model import GuideFile
from manudux.models.guidestep_model import GuideStep
from manudux.models.location_model import Location
from manudux.models.locationtype_model import LocationType
from manudux.models.maintenancelog_model import MaintenanceLog
from manudux.models.maintenancetask_model import MaintenanceTask
from manudux.models.property_model import Property
from manudux.models.property_type_model import PropertyType
from manudux.models.propertydocument_model import PropertyDocument


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1


class PropertyDocumentInline(admin.TabularInline):
    model = PropertyDocument
    extra = 0
    fields = ("name", "category", "file", "notes")


class ApplianceDocumentInline(admin.TabularInline):
    model = ApplianceDocument
    extra = 0
    fields = ("name", "category", "file", "notes")


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
    search_fields = ("name", "address", "city", "state", "zip_code", "parcel_number")
    ordering = ("name", "created_at", "updated_at")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    inlines = [LocationInline, PropertyDocumentInline]

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
    list_display = (
        "name",
        "property",
        "location_type",
        "created_at",
        "updated_at",
        "activated",
    )
    list_filter = ("location_type", "created_at", "updated_at", "activated")
    search_fields = ("name", "property")
    ordering = ("name", "created_at", "updated_at")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)


class GuideFileInline(admin.StackedInline):
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
    inlines = [GuideStepInline, GuideFileInline]


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


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "appliance_type",
        "brand",
        "warranty_expires",
        "activated",
    )
    list_filter = ("appliance_type", "activated", "brand")
    search_fields = ("name", "brand", "model_number", "serial_number", "location__name")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ApplianceDocumentInline]


@admin.register(ApplianceType)
class ApplianceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(ApplianceDocument)
class ApplianceDocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "appliance", "category", "uploaded_at")
    list_filter = ("category", "uploaded_at")
    search_fields = ("name", "appliance__name", "notes")


class MaintenanceLogInline(admin.TabularInline):
    model = MaintenanceLog
    extra = 0
    fields = ("completed_at", "completed_by", "notes", "cost")
    readonly_fields = ("completed_at", "completed_by", "notes", "cost")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "property", "due_date", "priority", "is_done")
    list_filter = ("priority", "is_done", "due_date")
    search_fields = ("title", "property__name", "location__name", "appliance__name")
    ordering = ("due_date",)
    readonly_fields = ("last_completed_at", "created_at", "updated_at")
    inlines = [MaintenanceLogInline]


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ("task_title", "property", "completed_at", "completed_by", "cost")
    list_filter = ("completed_at",)
    search_fields = ("task_title", "property__name", "notes")


@admin.register(PropertyDocument)
class PropertyDocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "property", "category", "uploaded_at")
    list_filter = ("category", "uploaded_at")
    search_fields = ("name", "property__name", "notes")
