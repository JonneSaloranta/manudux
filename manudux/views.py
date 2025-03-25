from django.shortcuts import render, get_object_or_404
from .models import Property, Location, Part, Appliance
from django.contrib.auth.decorators import login_required, permission_required
from .forms import PropertyForm, LocationForm
from django.shortcuts import redirect


def index(request):
    context = {}
    return render(request, 'manudux/index.html', context)

def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manudux:properties')
    else:
        form = PropertyForm()
    context = {
        'form': form
        }
    return render(request, 'manudux/property-create.html', context)

@login_required(login_url='/accounts/login/')
def properties(request):
    properties = Property.objects.all()
    return render(request, 'manudux/properties.html', {'properties': properties})

@permission_required('manudux.view_property', raise_exception=True)
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    locations = property.locations.all()  # Using related_name for efficient querying
    return render(request, 'manudux/property.html', {'property': property, 'locations': locations})

def locations(request):
    locations = Location.objects.all()
    return render(request, 'manudux/locations.html', {'locations': locations})

def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    appliances = location.appliances.all()  # Using related_name to fetch appliances
    return render(request, 'manudux/location.html', {'location': location, 'appliances': appliances})

def parts(request):
    parts = Part.objects.all()
    return render(request, 'manudux/parts.html', {'parts': parts})

def part_detail(request, pk):
    part = get_object_or_404(Part, pk=pk)
    return render(request, 'manudux/part.html', {'part': part})

def appliances(request):
    appliances = Appliance.objects.all()
    return render(request, 'manudux/appliances.html', {'appliances': appliances})

def appliance_detail(request, pk):
    appliance = get_object_or_404(Appliance, pk=pk)
    parts = appliance.parts.all()  # Get all parts related to the appliance
    return render(request, 'manudux/appliance.html', {'appliance': appliance, 'parts': parts})