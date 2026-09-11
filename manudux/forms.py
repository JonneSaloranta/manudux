from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, ModelForm
from django.utils.translation import gettext_lazy as _

from .models import (
    Appliance,
    ApplianceDocument,
    ApplianceType,
    Guide,
    GuideFile,
    GuideStep,
    Location,
    LocationType,
    MaintenanceTask,
    Property,
    PropertyDocument,
    PropertyType,
)
from .validators import validate_maintenance_receipt


class RegisterForm(UserCreationForm):
    email = EmailField(required=True, label=_("Email"))
    first_name = CharField(label=_("first name"))
    last_name = CharField(label=_("last name"))

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = [
            "name",
            "description",
            "image",
            "address",
            "city",
            "state",
            "zip_code",
            "property_type",
            "parcel_number",
            "year_built",
            "size_sqm",
            "lot_size_sqm",
            "purchase_date",
            "purchase_price",
            "estimated_value",
            "insurance_company",
            "insurance_policy_number",
            "insurance_expires",
            "guide",
            "activated",
        ]
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "insurance_expires": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "name": _("Property Name"),
            "description": _("Description"),
            "image": _("Image"),
            "address": _("Address"),
            "city": _("City"),
            "state": _("State"),
            "zip_code": _("Zip Code"),
            "property_type": _("Property Type"),
            "parcel_number": _("Parcel Number"),
            "year_built": _("Year Built"),
            "size_sqm": _("Living Area (m²)"),
            "lot_size_sqm": _("Lot Size (m²)"),
            "purchase_date": _("Purchase Date"),
            "purchase_price": _("Purchase Price"),
            "estimated_value": _("Estimated Value"),
            "insurance_company": _("Insurance Company"),
            "insurance_policy_number": _("Insurance Policy Number"),
            "insurance_expires": _("Insurance Expires"),
            "guide": _("Manual"),
            "activated": _("Activated"),
        }
        help_texts = {
            "name": _("Enter the name of the property."),
            "description": _("Enter a description of the property."),
            "image": _("Upload an image of the property."),
            "address": _("Enter the address of the property."),
            "city": _("Enter the city of the property."),
            "state": _("Enter the state of the property."),
            "zip_code": _("Enter the zip code of the property."),
            "property_type": _("Select the type of property."),
            "parcel_number": _("The property's registry/parcel identifier."),
            "guide": _("Optionally link an existing guide as this property's manual."),
            "activated": _("Check to activate the property."),
        }

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get("zip_code")
        if zip_code:
            try:
                is_negative = int(zip_code) < 0
            except ValueError:
                is_negative = False  # non-numeric postal codes are allowed
            if is_negative:
                raise ValidationError(_("Zipcode should be a positive integer"))
        return zip_code


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = [
            "name",
            "description",
            "image",
            "property",
            "location_type",
            "guide",
        ]
        labels = {
            "name": _("Location Name"),
            "description": _("Description"),
            "image": _("Image"),
            "property": _("Property"),
            "location_type": _("Location Type"),
            "guide": _("Manual"),
        }
        help_texts = {
            "name": _("Enter the name of the location."),
            "description": _("Enter a description of the location."),
            "image": _("Upload an image of the location."),
            "property": _("Select the property associated with this location."),
            "location_type": _(
                "What kind of space this is, e.g. garage, boiler room, storage."
            ),
            "guide": _("Optionally link an existing guide as this location's manual."),
        }


class LocationTypeForm(ModelForm):
    class Meta:
        model = LocationType
        fields = ["name", "description"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }
        help_texts = {
            "name": _("E.g. garage, boiler room, storage."),
            "description": _("Optional extra detail about this type."),
        }


class PropertyTypeForm(ModelForm):
    class Meta:
        model = PropertyType
        fields = ["name", "description"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }
        help_texts = {
            "name": _("E.g. residential, commercial."),
            "description": _("Optional extra detail about this type."),
        }


class GuideForm(ModelForm):
    class Meta:
        model = Guide
        fields = ["name", "description"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }
        help_texts = {
            "name": _("Enter a name for this guide."),
            "description": _("A short description of what this guide covers."),
        }


class GuideStepForm(ModelForm):
    class Meta:
        model = GuideStep
        fields = ["step_number", "title", "description", "image", "video"]
        labels = {
            "step_number": _("Step Number"),
            "title": _("Title"),
            "description": _("Description"),
            "image": _("Image"),
            "video": _("Video URL"),
        }
        help_texts = {
            "step_number": _("The order this step appears in."),
            "video": _("Optional link to a video for this step."),
        }


class GuideFileForm(ModelForm):
    class Meta:
        model = GuideFile
        fields = ["name", "file"]
        labels = {
            "name": _("Name"),
            "file": _("File"),
        }
        help_texts = {
            "file": _("PDF, Word, or image file."),
        }


class ApplianceForm(ModelForm):
    class Meta:
        model = Appliance
        fields = [
            "name",
            "location",
            "appliance_type",
            "brand",
            "model_number",
            "serial_number",
            "purchase_date",
            "warranty_expires",
            "notes",
            "image",
            "guide",
            "activated",
        ]
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "warranty_expires": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "name": _("Appliance Name"),
            "location": _("Location"),
            "appliance_type": _("Appliance Type"),
            "brand": _("Brand"),
            "model_number": _("Model Number"),
            "serial_number": _("Serial Number"),
            "purchase_date": _("Purchase Date"),
            "warranty_expires": _("Warranty Expires"),
            "notes": _("Notes"),
            "image": _("Image"),
            "guide": _("Manual"),
            "activated": _("Activated"),
        }
        help_texts = {
            "name": _("Enter the name of the appliance."),
            "location": _("Select the location this appliance is at."),
            "appliance_type": _(
                "What kind of appliance this is, e.g. HVAC, kitchen, water heater."
            ),
            "guide": _("Optionally link an existing guide as this appliance's manual."),
            "activated": _("Check to keep this appliance active."),
        }


class ApplianceTypeForm(ModelForm):
    class Meta:
        model = ApplianceType
        fields = ["name", "description"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }
        help_texts = {
            "name": _("E.g. HVAC, kitchen, water heater."),
            "description": _("Optional extra detail about this type."),
        }


class ApplianceDocumentForm(ModelForm):
    class Meta:
        model = ApplianceDocument
        fields = ["name", "category", "file", "notes"]
        labels = {
            "name": _("Document Name"),
            "category": _("Category"),
            "file": _("File"),
            "notes": _("Notes"),
        }
        help_texts = {
            "name": _('E.g. "Purchase receipt" or "Warranty certificate".'),
            "file": _("PDF, Word, Excel, or an image scan (max 25MB)."),
        }


class MaintenanceTaskForm(ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = [
            "title",
            "description",
            "property",
            "location",
            "appliance",
            "due_date",
            "priority",
            "recurrence_interval_days",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": _("Title"),
            "description": _("Description"),
            "property": _("Property"),
            "location": _("Location"),
            "appliance": _("Appliance"),
            "due_date": _("Due Date"),
            "priority": _("Priority"),
            "recurrence_interval_days": _("Repeat every (days)"),
        }
        help_texts = {
            "location": _("Optional: narrow this task down to a specific location."),
            "appliance": _("Optional: narrow this task down to a specific appliance."),
            "recurrence_interval_days": _(
                "Leave blank for a one-off task, or enter a number of days to repeat it."
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        property_obj = cleaned_data.get("property")
        location = cleaned_data.get("location")
        appliance = cleaned_data.get("appliance")

        if property_obj and location and location.property_id != property_obj.id:
            self.add_error(
                "location", _("The selected location does not belong to this property.")
            )
        if (
            property_obj
            and appliance
            and appliance.location.property_id != property_obj.id
        ):
            self.add_error(
                "appliance",
                _("The selected appliance does not belong to this property."),
            )
        return cleaned_data


class MaintenanceCompletionForm(forms.Form):
    notes = forms.CharField(
        label=_("Notes"), required=False, widget=forms.Textarea(attrs={"rows": 3})
    )
    cost = forms.DecimalField(
        label=_("Cost"), required=False, max_digits=10, decimal_places=2, min_value=0
    )
    receipt = forms.FileField(
        label=_("Receipt"),
        required=False,
        validators=[validate_maintenance_receipt],
        help_text=_(
            "Optional: attach a receipt or invoice (PDF, Word, Excel, or an image)."
        ),
    )


class PropertyDocumentForm(ModelForm):
    class Meta:
        model = PropertyDocument
        fields = ["name", "category", "file", "notes"]
        labels = {
            "name": _("Document Name"),
            "category": _("Category"),
            "file": _("File"),
            "notes": _("Notes"),
        }
        help_texts = {
            "name": _('E.g. "Deed of sale" or "Home insurance policy 2026".'),
            "file": _("PDF, Word, Excel, or an image scan (max 25MB)."),
        }
