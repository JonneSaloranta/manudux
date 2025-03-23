from django.shortcuts import render, get_object_or_404
from .models import Property, Location, Part, Appliance
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    return render(request, 'manudux/index.html')