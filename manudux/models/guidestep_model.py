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


class GuideStep(models.Model):
    """
    A model for creating steps for a guide.

    Fields:
        guide (ForeignKey): The main guide object.
        step_number (PositiveIntegerField): Guide step number.
        title (CharField): Step title
        description (TextField): Step Description
        image (ImageField): Step Image
        video (URLField): Step Video
        created_at (DateTimeField): Auto generated creation date
        updated_at (DateTimeField): Auto generated update date
    """

    guide = models.ForeignKey("Guide", related_name="steps", on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="guides/steps", blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ["step_number"]

    def __str__(self):
        return f"Step {self.step_number} for {self.guide.name}"

    class Meta:
        verbose_name = _("Guide step")
        verbose_name_plural = _("Guide steps")
