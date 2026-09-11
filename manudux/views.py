from datetime import timedelta

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import (
    ApplianceForm,
    GuideFileForm,
    GuideForm,
    GuideStepForm,
    LocationForm,
    LocationTypeForm,
    MaintenanceCompletionForm,
    MaintenanceTaskForm,
    PropertyDocumentForm,
    PropertyForm,
    PropertyTypeForm,
    RegisterForm,
)
from .models import (
    Appliance,
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

PAGE_SIZE = 20
DASHBOARD_TASK_LIMIT = 10


def index(request):
    context = {}

    if request.user.is_authenticated:
        today = timezone.localdate()
        lookahead = today + timedelta(days=settings.MAINTENANCE_REMINDER_LOOKAHEAD_DAYS)
        active_tasks = MaintenanceTask.objects.filter(is_done=False).select_related(
            "property"
        )
        context["overdue_tasks"] = active_tasks.filter(due_date__lt=today)[
            :DASHBOARD_TASK_LIMIT
        ]
        context["upcoming_tasks"] = active_tasks.filter(
            due_date__gte=today, due_date__lte=lookahead
        )[:DASHBOARD_TASK_LIMIT]

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
        "form": form,
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
    documents = property.documents.all()
    return render(
        request,
        "manudux/property.html",
        {"property": property, "locations": locations, "documents": documents},
    )


@login_required(login_url="/accounts/login/")
def create_property_document(request, property_pk):
    property_obj = get_object_or_404(Property, pk=property_pk)

    if request.method == "POST":
        form = PropertyDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.property = property_obj
            document.save()
            return redirect("manudux:property", pk=property_obj.pk)
    else:
        form = PropertyDocumentForm()

    context = {"form": form, "property": property_obj}
    return render(request, "manudux/property-document-create.html", context)


@login_required(login_url="/accounts/login/")
def delete_property_document(request, pk):
    document = get_object_or_404(PropertyDocument, pk=pk)
    if request.method == "POST":
        property_pk = document.property_id
        document.delete()
        return redirect("manudux:property", pk=property_pk)
    context = {"document": document}
    return render(request, "manudux/property-document-delete.html", context)


@login_required(login_url="/accounts/login/")
def property_types(request):
    queryset = PropertyType.objects.order_by("name")
    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))
    context = {"property_types": page_obj, "page_obj": page_obj}
    return render(request, "manudux/property-types.html", context)


@login_required(login_url="/accounts/login/")
def create_property_type(request):
    if request.method == "POST":
        form = PropertyTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manudux:property-types")
    else:
        form = PropertyTypeForm()
    context = {"form": form}
    return render(request, "manudux/property-type-create.html", context)


@login_required(login_url="/accounts/login/")
def edit_property_type(request, pk):
    property_type = get_object_or_404(PropertyType, pk=pk)
    if request.method == "POST":
        form = PropertyTypeForm(request.POST, instance=property_type)
        if form.is_valid():
            form.save()
            return redirect("manudux:property-types")
    else:
        form = PropertyTypeForm(instance=property_type)
    context = {"form": form, "property_type": property_type}
    return render(request, "manudux/property-type-edit.html", context)


@login_required(login_url="/accounts/login/")
def delete_property_type(request, pk):
    return delete_obj(
        request,
        pk,
        PropertyType,
        "manudux:property-types",
        "manudux/property-type-delete.html",
        "property_type",
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
    queryset = Location.objects.filter(activated=True).order_by("name")
    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))
    return render(
        request, "manudux/locations.html", {"locations": page_obj, "page_obj": page_obj}
    )


@login_required(login_url="/accounts/login/")
def location_types(request):
    queryset = LocationType.objects.order_by("name")
    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))
    context = {"location_types": page_obj, "page_obj": page_obj}
    return render(request, "manudux/location-types.html", context)


@login_required(login_url="/accounts/login/")
def create_location_type(request):
    if request.method == "POST":
        form = LocationTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manudux:location-types")
    else:
        form = LocationTypeForm()
    context = {"form": form}
    return render(request, "manudux/location-type-create.html", context)


@login_required(login_url="/accounts/login/")
def edit_location_type(request, pk):
    location_type = get_object_or_404(LocationType, pk=pk)
    if request.method == "POST":
        form = LocationTypeForm(request.POST, instance=location_type)
        if form.is_valid():
            form.save()
            return redirect("manudux:location-types")
    else:
        form = LocationTypeForm(instance=location_type)
    context = {"form": form, "location_type": location_type}
    return render(request, "manudux/location-type-edit.html", context)


@login_required(login_url="/accounts/login/")
def delete_location_type(request, pk):
    return delete_obj(
        request,
        pk,
        LocationType,
        "manudux:location-types",
        "manudux/location-type-delete.html",
        "location_type",
    )


@login_required(login_url="/accounts/login/")
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    appliances = location.appliances.filter(activated=True)
    return render(
        request,
        "manudux/location.html",
        {"location": location, "appliances": appliances},
    )


def delete_obj(request, pk, model, redirect_url, template, context_name):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect(redirect_url)
    context = {context_name: obj}
    return render(request, template, context)


@login_required(login_url="/accounts/login/")
def appliances(request):
    queryset = Appliance.objects.filter(activated=True).order_by("name")
    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))
    return render(
        request,
        "manudux/appliances.html",
        {"appliances": page_obj, "page_obj": page_obj},
    )


@login_required(login_url="/accounts/login/")
def create_appliance(request):
    location_obj = None
    location_id = request.GET.get("location_id")

    if location_id:
        location_obj = get_object_or_404(Location, id=location_id)

    if request.method == "POST":
        form = ApplianceForm(request.POST, request.FILES)
        if form.is_valid():
            appliance = form.save(commit=False)
            if location_obj:
                appliance.location = location_obj
            appliance.save()
            return redirect("manudux:appliance", pk=appliance.pk)
    else:
        form = ApplianceForm(initial={"location": location_obj})

    context = {"form": form, "location": location_obj}
    return render(request, "manudux/appliance-create.html", context)


@login_required(login_url="/accounts/login/")
def appliance_detail(request, pk):
    appliance = get_object_or_404(Appliance, pk=pk)
    tasks = appliance.maintenance_tasks.all()
    return render(
        request,
        "manudux/appliance.html",
        {"appliance": appliance, "maintenance_tasks": tasks},
    )


@login_required(login_url="/accounts/login/")
def edit_appliance(request, pk):
    appliance = get_object_or_404(Appliance, pk=pk)
    if request.method == "POST":
        form = ApplianceForm(request.POST, request.FILES, instance=appliance)
        if form.is_valid():
            form.save()
            return redirect("manudux:appliance", pk=pk)
    else:
        form = ApplianceForm(instance=appliance)
    context = {"form": form, "appliance": appliance}
    return render(request, "manudux/appliance-edit.html", context)


@login_required(login_url="/accounts/login/")
def delete_appliance(request, pk):
    return delete_obj(
        request,
        pk,
        Appliance,
        "manudux:appliances",
        "manudux/appliance-delete.html",
        "appliance",
    )


@login_required(login_url="/accounts/login/")
def maintenance_tasks(request):
    status = request.GET.get("filter", "active")
    queryset = MaintenanceTask.objects.select_related(
        "property", "location", "appliance"
    )

    if status == "done":
        queryset = queryset.filter(is_done=True)
    elif status == "overdue":
        queryset = queryset.filter(is_done=False, due_date__lt=timezone.localdate())
    else:
        status = "active"
        queryset = queryset.filter(is_done=False)

    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))
    context = {
        "maintenance_tasks": page_obj,
        "page_obj": page_obj,
        "status": status,
        "today": timezone.localdate(),
    }
    return render(request, "manudux/maintenance-tasks.html", context)


@login_required(login_url="/accounts/login/")
def create_maintenance_task(request):
    initial = {}
    property_obj = None

    property_id = request.GET.get("property_id")
    location_id = request.GET.get("location_id")
    appliance_id = request.GET.get("appliance_id")

    if appliance_id:
        appliance_obj = get_object_or_404(Appliance, id=appliance_id)
        initial["appliance"] = appliance_obj
        initial["location"] = appliance_obj.location
        property_obj = appliance_obj.location.property
    elif location_id:
        location_obj = get_object_or_404(Location, id=location_id)
        initial["location"] = location_obj
        property_obj = location_obj.property
    elif property_id:
        property_obj = get_object_or_404(Property, id=property_id)

    if property_obj:
        initial["property"] = property_obj

    if request.method == "POST":
        form = MaintenanceTaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect("manudux:maintenance-task", pk=task.pk)
    else:
        form = MaintenanceTaskForm(initial=initial)

    context = {"form": form, "property": property_obj}
    return render(request, "manudux/maintenance-task-create.html", context)


@login_required(login_url="/accounts/login/")
def maintenance_task_detail(request, pk):
    task = get_object_or_404(MaintenanceTask, pk=pk)

    if request.method == "POST":
        completion_form = MaintenanceCompletionForm(request.POST)
        if completion_form.is_valid():
            task.mark_complete(
                request.user,
                notes=completion_form.cleaned_data["notes"],
                cost=completion_form.cleaned_data["cost"],
            )
            return redirect("manudux:maintenance-task", pk=pk)
    else:
        completion_form = MaintenanceCompletionForm()

    context = {
        "task": task,
        "logs": task.logs.all(),
        "completion_form": completion_form,
        "today": timezone.localdate(),
    }
    return render(request, "manudux/maintenance-task.html", context)


@login_required(login_url="/accounts/login/")
def edit_maintenance_task(request, pk):
    task = get_object_or_404(MaintenanceTask, pk=pk)
    if request.method == "POST":
        form = MaintenanceTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("manudux:maintenance-task", pk=pk)
    else:
        form = MaintenanceTaskForm(instance=task)
    context = {"form": form, "task": task}
    return render(request, "manudux/maintenance-task-edit.html", context)


@login_required(login_url="/accounts/login/")
def delete_maintenance_task(request, pk):
    return delete_obj(
        request,
        pk,
        MaintenanceTask,
        "manudux:maintenance-tasks",
        "manudux/maintenance-task-delete.html",
        "task",
    )


@login_required(login_url="/accounts/login/")
def guide_list(request):
    queryset = Guide.objects.order_by("name")
    page_obj = Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))
    context = {"guides": page_obj, "page_obj": page_obj}
    return render(request, "manudux/guide-list.html", context=context)


@login_required(login_url="/accounts/login/")
def guide_detail(request, pk):
    guide = get_object_or_404(Guide, pk=pk)

    # What this guide is actually linked from - Property/Location/Appliance
    # each have an optional FK to Guide (not the other way around), so this
    # is built from their reverse managers rather than a field on Guide.
    used_by = []
    for prop in guide.property_set.all():
        used_by.append(
            {
                "label": str(prop),
                "url": reverse("manudux:property", kwargs={"pk": prop.pk}),
            }
        )
    for location in guide.location_set.all():
        used_by.append(
            {
                "label": str(location),
                "url": reverse("manudux:location", kwargs={"pk": location.pk}),
            }
        )
    for appliance in guide.appliance_set.all():
        used_by.append(
            {
                "label": str(appliance),
                "url": reverse("manudux:appliance", kwargs={"pk": appliance.pk}),
            }
        )

    context = {"guide": guide, "used_by": used_by}

    return render(request, "manudux/guide-details.html", context=context)


@login_required(login_url="/accounts/login/")
def create_guide(request):
    if request.method == "POST":
        form = GuideForm(request.POST)
        if form.is_valid():
            guide = form.save()
            return redirect("manudux:guide", pk=guide.pk)
    else:
        form = GuideForm()
    context = {"form": form}
    return render(request, "manudux/guide-create.html", context)


@login_required(login_url="/accounts/login/")
def edit_guide(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    if request.method == "POST":
        form = GuideForm(request.POST, instance=guide)
        if form.is_valid():
            form.save()
            return redirect("manudux:guide", pk=pk)
    else:
        form = GuideForm(instance=guide)
    context = {"form": form, "guide": guide}
    return render(request, "manudux/guide-edit.html", context)


@login_required(login_url="/accounts/login/")
def delete_guide(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    if request.method == "POST":
        # GuideFile.guide is on_delete=PROTECT, so any attached files have
        # to go first or guide.delete() below would raise ProtectedError.
        guide.guidefile_set.all().delete()
        guide.delete()
        return redirect("manudux:guides")
    context = {"guide": guide}
    return render(request, "manudux/guide-delete.html", context)


@login_required(login_url="/accounts/login/")
def create_guide_step(request, guide_pk):
    guide = get_object_or_404(Guide, pk=guide_pk)
    next_step_number = guide.steps.count() + 1

    if request.method == "POST":
        form = GuideStepForm(request.POST, request.FILES)
        if form.is_valid():
            step = form.save(commit=False)
            step.guide = guide
            step.save()
            return redirect("manudux:guide", pk=guide.pk)
    else:
        form = GuideStepForm(initial={"step_number": next_step_number})

    context = {"form": form, "guide": guide}
    return render(request, "manudux/guide-step-create.html", context)


@login_required(login_url="/accounts/login/")
def edit_guide_step(request, pk):
    step = get_object_or_404(GuideStep, pk=pk)
    if request.method == "POST":
        form = GuideStepForm(request.POST, request.FILES, instance=step)
        if form.is_valid():
            form.save()
            return redirect("manudux:guide", pk=step.guide_id)
    else:
        form = GuideStepForm(instance=step)
    context = {"form": form, "step": step}
    return render(request, "manudux/guide-step-edit.html", context)


@login_required(login_url="/accounts/login/")
def delete_guide_step(request, pk):
    step = get_object_or_404(GuideStep, pk=pk)
    if request.method == "POST":
        guide_pk = step.guide_id
        step.delete()
        return redirect("manudux:guide", pk=guide_pk)
    context = {"step": step}
    return render(request, "manudux/guide-step-delete.html", context)


@login_required(login_url="/accounts/login/")
def move_guide_step(request, pk, direction):
    """Swap a step's position with its previous/next sibling. The
    keyboard/screen-reader-accessible way to reorder steps - always
    rendered as plain buttons, no JS required."""
    step = get_object_or_404(GuideStep, pk=pk)
    if request.method == "POST" and direction in ("up", "down"):
        siblings = step.guide.steps
        if direction == "up":
            neighbor = siblings.filter(step_number__lt=step.step_number).last()
        else:
            neighbor = siblings.filter(step_number__gt=step.step_number).first()
        if neighbor:
            step.step_number, neighbor.step_number = (
                neighbor.step_number,
                step.step_number,
            )
            step.save(update_fields=["step_number"])
            neighbor.save(update_fields=["step_number"])
    return redirect("manudux:guide", pk=step.guide_id)


@login_required(login_url="/accounts/login/")
def reorder_guide_steps(request, guide_pk):
    """Persist a full new step order, posted as a repeated step_id field in
    the desired order. Used by the drag-to-reorder JS in scripts.js."""
    guide = get_object_or_404(Guide, pk=guide_pk)
    if request.method == "POST":
        steps_by_id = {step.pk: step for step in guide.steps.all()}
        for position, raw_step_id in enumerate(
            request.POST.getlist("step_id"), start=1
        ):
            step = steps_by_id.get(int(raw_step_id))
            if step and step.step_number != position:
                step.step_number = position
                step.save(update_fields=["step_number"])
    return redirect("manudux:guide", pk=guide.pk)


@login_required(login_url="/accounts/login/")
def create_guide_file(request, guide_pk):
    guide = get_object_or_404(Guide, pk=guide_pk)

    if request.method == "POST":
        form = GuideFileForm(request.POST, request.FILES)
        if form.is_valid():
            guide_file = form.save(commit=False)
            guide_file.guide = guide
            guide_file.save()
            return redirect("manudux:guide", pk=guide.pk)
    else:
        form = GuideFileForm()

    context = {"form": form, "guide": guide}
    return render(request, "manudux/guide-file-create.html", context)


@login_required(login_url="/accounts/login/")
def delete_guide_file(request, pk):
    guide_file = get_object_or_404(GuideFile, pk=pk)
    if request.method == "POST":
        guide_pk = guide_file.guide_id
        guide_file.delete()
        return redirect("manudux:guide", pk=guide_pk)
    context = {"guide_file": guide_file}
    return render(request, "manudux/guide-file-delete.html", context)
