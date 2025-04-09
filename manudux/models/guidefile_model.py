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
from . import Guide

class GuideFile(models.Model):
    name = models.CharField(max_length=255)
    guide = models.ForeignKey(Guide, on_delete=models.PROTECT)
    file = models.FileField(upload_to="guides/files/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Guide file")
        verbose_name_plural = _("Guide files")
