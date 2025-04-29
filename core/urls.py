from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from schema_graph.views import Schema
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include(("manudux.urls", "manudux"), namespace="manudux")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if  settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        path("schema/", Schema.as_view()),
    ] + debug_toolbar_urls()
