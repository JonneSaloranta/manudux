import re

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from schema_graph.views import Schema
from debug_toolbar.toolbar import debug_toolbar_urls

# Media (user-uploaded) files have no dedicated web server or CDN in front of
# this project, so they are served by Django itself in every environment.
# django.conf.urls.static.static() only wires this up when DEBUG=True, which
# left uploaded property images, guide files and QR codes unreachable in
# production - hence the explicit pattern below instead of that helper.
media_urlpatterns = [
    re_path(
        r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(("django.contrib.auth.urls", "accounts"), namespace="accounts")),
    path("", include(("manudux.urls", "manudux"), namespace="manudux")),
] + media_urlpatterns

if settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        path("schema/", Schema.as_view()),
    ] + debug_toolbar_urls()
