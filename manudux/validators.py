from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileExtensionAndSizeValidator:
    """Rejects uploads with a disallowed extension or over a size limit."""

    def __init__(self, allowed_extensions, max_size_mb):
        self.allowed_extensions = {ext.lower() for ext in allowed_extensions}
        self.max_size_mb = max_size_mb

    def __call__(self, value):
        extension = value.name.rsplit(".", 1)[-1].lower() if "." in value.name else ""
        if extension not in self.allowed_extensions:
            raise ValidationError(
                _("Unsupported file type: .%(extension)s"),
                params={"extension": extension},
            )

        max_bytes = self.max_size_mb * 1024 * 1024
        if value.size > max_bytes:
            raise ValidationError(
                _("File is too large; the maximum size is %(max_size_mb)s MB."),
                params={"max_size_mb": self.max_size_mb},
            )

    def __eq__(self, other):
        return (
            isinstance(other, FileExtensionAndSizeValidator)
            and self.allowed_extensions == other.allowed_extensions
            and self.max_size_mb == other.max_size_mb
        )


validate_guide_file = FileExtensionAndSizeValidator(
    allowed_extensions=[
        "pdf",
        "doc",
        "docx",
        "txt",
        "png",
        "jpg",
        "jpeg",
        "gif",
        "svg",
        "mp4",
        "zip",
    ],
    max_size_mb=25,
)

# Deeds, insurance certificates, inspection reports, floor plans - scans and
# office documents, not the broader media types guides accept.
validate_property_document = FileExtensionAndSizeValidator(
    allowed_extensions=["pdf", "doc", "docx", "xlsx", "jpg", "jpeg", "png"],
    max_size_mb=25,
)

# Receipts, warranty certificates, manuals - same shape as property documents.
validate_appliance_document = FileExtensionAndSizeValidator(
    allowed_extensions=["pdf", "doc", "docx", "xlsx", "jpg", "jpeg", "png"],
    max_size_mb=25,
)

# A receipt/invoice attached to a completed maintenance log entry.
validate_maintenance_receipt = FileExtensionAndSizeValidator(
    allowed_extensions=["pdf", "doc", "docx", "xlsx", "jpg", "jpeg", "png"],
    max_size_mb=25,
)
