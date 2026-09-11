from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.sign_up, name="register"),
    path("site-settings/", views.site_settings, name="site-settings"),
    path("properties/", views.properties, name="properties"),
    path("properties/create-property/", views.create_property, name="create-property"),
    path("property/<int:pk>/edit/", views.edit_property, name="edit-property"),
    path("property/<int:pk>/delete/", views.delete_property, name="delete-property"),
    path(
        "property/<int:property_pk>/documents/create/",
        views.create_property_document,
        name="create-property-document",
    ),
    path(
        "property-document/<int:pk>/delete/",
        views.delete_property_document,
        name="delete-property-document",
    ),
    path("property/<int:pk>/", views.property_detail, name="property"),
    path("properties/types/", views.property_types, name="property-types"),
    path(
        "properties/types/create/",
        views.create_property_type,
        name="create-property-type",
    ),
    path(
        "property-type/<int:pk>/edit/",
        views.edit_property_type,
        name="edit-property-type",
    ),
    path(
        "property-type/<int:pk>/delete/",
        views.delete_property_type,
        name="delete-property-type",
    ),
    path("locations/create-location/", views.create_location, name="create-location"),
    path("location/<int:pk>/edit/", views.edit_location, name="edit-location"),
    path("location/<int:pk>/delete/", views.delete_location, name="delete-location"),
    path("locations/", views.locations, name="locations"),
    path("locations/types/", views.location_types, name="location-types"),
    path(
        "locations/types/create/",
        views.create_location_type,
        name="create-location-type",
    ),
    path(
        "location-type/<int:pk>/edit/",
        views.edit_location_type,
        name="edit-location-type",
    ),
    path(
        "location-type/<int:pk>/delete/",
        views.delete_location_type,
        name="delete-location-type",
    ),
    path("location/<int:pk>/", views.location_detail, name="location"),
    path("guides/", views.guide_list, name="guides"),
    path("guides/create-guide/", views.create_guide, name="create-guide"),
    path("guide/<int:pk>/edit/", views.edit_guide, name="edit-guide"),
    path("guide/<int:pk>/delete/", views.delete_guide, name="delete-guide"),
    path(
        "guide/<int:guide_pk>/steps/create/",
        views.create_guide_step,
        name="create-guide-step",
    ),
    path("guide-step/<int:pk>/edit/", views.edit_guide_step, name="edit-guide-step"),
    path(
        "guide-step/<int:pk>/delete/",
        views.delete_guide_step,
        name="delete-guide-step",
    ),
    path(
        "guide-step/<int:pk>/move/<str:direction>/",
        views.move_guide_step,
        name="move-guide-step",
    ),
    path(
        "guide/<int:guide_pk>/steps/reorder/",
        views.reorder_guide_steps,
        name="reorder-guide-steps",
    ),
    path(
        "guide/<int:guide_pk>/files/create/",
        views.create_guide_file,
        name="create-guide-file",
    ),
    path(
        "guide-file/<int:pk>/delete/",
        views.delete_guide_file,
        name="delete-guide-file",
    ),
    path("guide/<int:pk>/", views.guide_detail, name="guide"),
    path("appliances/", views.appliances, name="appliances"),
    path(
        "appliances/create-appliance/", views.create_appliance, name="create-appliance"
    ),
    path("appliance/<int:pk>/edit/", views.edit_appliance, name="edit-appliance"),
    path("appliance/<int:pk>/delete/", views.delete_appliance, name="delete-appliance"),
    path("appliance/<int:pk>/", views.appliance_detail, name="appliance"),
    path("maintenance/", views.maintenance_tasks, name="maintenance-tasks"),
    path(
        "maintenance/create-task/",
        views.create_maintenance_task,
        name="create-maintenance-task",
    ),
    path(
        "maintenance/<int:pk>/edit/",
        views.edit_maintenance_task,
        name="edit-maintenance-task",
    ),
    path(
        "maintenance/<int:pk>/delete/",
        views.delete_maintenance_task,
        name="delete-maintenance-task",
    ),
    path(
        "maintenance/<int:pk>/",
        views.maintenance_task_detail,
        name="maintenance-task",
    ),
]
