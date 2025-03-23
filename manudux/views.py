from django.shortcuts import render, get_object_or_404
from .models import Property, Location, Part, Appliance
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    context = {}
    return render(request, 'manudux/index.html', context)

@login_required(login_url='/accounts/login/')
def properties(request):
    properties = Property.objects.all()
    return render(request, 'manudux/properties.html', {'properties': properties})

@permission_required('manudux.view_property', raise_exception=True)
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    locations = property.locations.all()  # Using related_name for efficient querying
    return render(request, 'manudux/property.html', {'property': property, 'locations': locations})
