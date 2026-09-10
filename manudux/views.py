from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Property, Location, Guide, GuideFile, GuideStep
from django.contrib.auth.decorators import login_required, permission_required
from .forms import PropertyForm, LocationForm
from django.shortcuts import redirect
from django.conf import settings
from .forms import RegisterForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout, authenticate

PAGE_SIZE = 20


def index(request):
    context = {}
    return render(request, "manudux/index.html", context)

def sign_up(request):
    if not settings.ALLOW_REGISTRATION:
        raise PermissionDenied()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("manudux:index")
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, "registration/signup.html", context=context)

@login_required
def site_settings(request):
    if request.user.is_superuser:
        return render(request, "manudux/site-settings.html")
    else:
        raise PermissionDenied()

@login_required(login_url=settings.LOGIN_URL)
def create_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("manudux:properties")
    else:
        form = PropertyForm()
    context = {"form": form}
    return render(request, "manudux/property-create.html", context)


@login_required(login_url="/accounts/login/")
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect("manudux:property", pk=pk)
    else:
        form = PropertyForm(instance=property)
    context = {"form": form, "property": property}
    return render(request, "manudux/property-edit.html", context)


@login_required(login_url="/accounts/login/")
def delete_property(request, pk):
    return delete_obj(
        request,
        pk,
        Property,
        "manudux:properties",
        "manudux/property-delete.html",
        "property",
    )


@login_required(login_url="/accounts/login/")
def properties(request):
    queryset = Property.objects.filter(activated=True).order_by("name")
    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))

    context = {"properties": page_obj, "page_obj": page_obj}

    return render(request, "manudux/properties.html", context=context)


@login_required(login_url="/accounts/login/")
# @permission_required('manudux.can_edit', raise_exception=True)
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    locations = property.locations.all()  # Using related_name for efficient querying
    return render(
        request, "manudux/property.html", {"property": property, "locations": locations}
    )


@login_required(login_url="/accounts/login/")
def create_location(request):
    property_obj = None
    property_id = request.GET.get("property_id")  # Get property_id from URL parameters

    if property_id:
        property_obj = get_object_or_404(Property, id=property_id)  # Fetch the property

    if request.method == "POST":
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.save(commit=False)
            if property_obj:
                location.property = property_obj  # Assign property before saving
            location.save()
            return redirect(
                "manudux:property", pk=location.property.id
            )  # Redirect to property detail

    else:
        form = LocationForm(
            initial={"property": property_obj}
        )  # Pre-fill the property field

    context = {
        "form": form,
        "property": property_obj,  # Pass the property to the template
    }
    return render(request, "manudux/location-create.html", context)


@login_required(login_url="/accounts/login/")
def edit_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        form = LocationForm(request.POST, request.FILES, instance=location)
        if form.is_valid():
            form.save()
            return redirect("manudux:location", pk=pk)
    else:
        form = LocationForm(instance=location)
    context = {"form": form, "location": location}
    return render(request, "manudux/location-edit.html", context)


@login_required(login_url="/accounts/login/")
def delete_location(request, pk):
    return delete_obj(
        request,
        pk,
        Location,
        "manudux:locations",
        "manudux/location-delete.html",
        "location",
    )


@login_required(login_url="/accounts/login/")
def locations(request):
    queryset = Location.objects.order_by("name")
    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))
    return render(
        request, "manudux/locations.html", {"locations": page_obj, "page_obj": page_obj}
    )


@login_required(login_url="/accounts/login/")
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    return render(request, "manudux/location.html", {"location": location})


def delete_obj(request, pk, model, redirect_url, template, context_name):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect(redirect_url)
    context = {context_name: obj}
    return render(request, template, context)


def guide_list(request):
    queryset = Guide.objects.order_by("name")
    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))
    context = {"guides": page_obj, "page_obj": page_obj}
    return render(request, "manudux/guide-list.html", context=context)


def guide_detail(request, pk):
    guide = get_object_or_404(Guide, pk=pk)

    context = {"guide": guide}

    return render(request, "manudux/guide-details.html", context=context)
