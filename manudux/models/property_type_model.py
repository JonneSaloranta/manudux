from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from django.urls import reverse
from django.conf import settings
from urllib.parse import urlencode
import textwrap
from django.conf import settings
import os

class PropertyType(models.Model):
    """Represents a type of property (e.g., residential, commercial)."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Property Type")
        verbose_name_plural = _("Property Types")
