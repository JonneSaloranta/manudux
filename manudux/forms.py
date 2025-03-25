from django.forms import ModelForm
from .models import Property, Location, Part, Appliance
from django.utils.translation import gettext_lazy as _

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'description', 'image', 'address', 'city', 'state', 'zip_code']
        labels = {
            'name': _('Property Name'),
            'description': _('Description'),
            'image': _('Image'),
            'address': _('Address'),
            'city': _('City'),
            'state': _('State'),
            'zip_code': _('Zip Code'),
        }
        help_texts = {
            'name': _('Enter the name of the property.'),
            'description': _('Enter a description of the property.'),
            'image': _('Upload an image of the property.'),
            'address': _('Enter the address of the property.'),
            'city': _('Enter the city of the property.'),
            'state': _('Enter the state of the property.'),
            'zip_code': _('Enter the zip code of the property.'),
        }

class LocationForm(ModelForm):
    # name = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    # property = models.ForeignKey(
    #     Property, on_delete=models.CASCADE, related_name='locations'
    # )
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # activated = models.BooleanField(default=True)

    class Meta:
        model = Location
        fields = ['name', 'description', 'property']
        labels = {
            'name': _('Location Name'),
            'description': _('Description'),
            'property': _('Property'),
        }
        help_texts = {
            'name': _('Enter the name of the location.'),
            'description': _('Enter a description of the location.'),
            'property': _('Select the property associated with this location.'),
        }