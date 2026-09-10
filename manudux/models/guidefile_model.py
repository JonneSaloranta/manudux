from django.db import models
from django.utils.translation import gettext_lazy as _
from . import Guide
from ..validators import validate_guide_file


class GuideFile(models.Model):
    name = models.CharField(max_length=255)
    guide = models.ForeignKey(Guide, on_delete=models.PROTECT)
    file = models.FileField(upload_to="guides/files/", validators=[validate_guide_file])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Guide file")
        verbose_name_plural = _("Guide files")
