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
    path("property/<int:pk>/", views.property_detail, name="property"),
    path("locations/create-location/", views.create_location, name="create-location"),
    path("location/<int:pk>/edit/", views.edit_location, name="edit-location"),
    path("location/<int:pk>/delete/", views.delete_location, name="delete-location"),
    path("locations/", views.locations, name="locations"),
    path("location/<int:pk>/", views.location_detail, name="location"),
    path("guides/", views.guide_list, name="guides"),
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
