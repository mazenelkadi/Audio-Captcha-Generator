from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

class FieldTypes(models.TextChoices):
    TEXT = "text", "Text"
    NUMBER = "number", "Number"
    DATE = "date", "Date"
    BOOLEAN = "boolean", "Boolean"
    SINGLE_SELECT = "single_select", "Single Select"
    MULTI_SELECT = "multi_select", "Multi Select"


class Base(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bases_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "created_by"]

    def __str__(self) -> str:  # pragma: no cover - repr helper
        return self.name


class BaseMembership(models.Model):
    class MembershipRole(models.TextChoices):
        ADMIN = "admin", "Admin"
        VIEWER = "viewer", "Viewer"

    base = models.ForeignKey(Base, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=16, choices=MembershipRole.choices, default=MembershipRole.VIEWER)

    class Meta:
        unique_together = ["base", "user"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user} -> {self.base} ({self.get_role_display()})"


class Field(models.Model):
    base = models.ForeignKey(Base, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=32, choices=FieldTypes.choices)
    is_required = models.BooleanField(default=False)
    options = models.JSONField(blank=True, default=dict, help_text="Additional metadata for select fields")
    order = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["order", "id"]
        unique_together = ["base", "name"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.field_type})"


class Record(models.Model):
    base = models.ForeignKey(Base, on_delete=models.CASCADE, related_name="records")
    data = models.JSONField(default=dict)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="records_created",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Record {self.pk} in {self.base_id}"

    def clean_data(self):
        """Ensure data conforms to the base field definitions."""
        validated = {}
        field_map = {field.name: field for field in self.base.fields.all()}
        for field_name, field in field_map.items():
            value = self.data.get(field_name)
            if value is None:
                if field.is_required:
                    raise ValueError(f"Field '{field_name}' is required")
                continue
            field_type = field.field_type
            if field_type == FieldTypes.NUMBER:
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Field '{field_name}' must be a number")
            elif field_type == FieldTypes.BOOLEAN:
                if not isinstance(value, bool):
                    raise ValueError(f"Field '{field_name}' must be a boolean")
            elif field_type == FieldTypes.SINGLE_SELECT:
                options = field.options.get("choices", [])
                if value not in options:
                    raise ValueError(f"Value '{value}' not valid for field '{field_name}'")
            elif field_type == FieldTypes.MULTI_SELECT:
                options = field.options.get("choices", [])
                if not isinstance(value, list) or not set(value).issubset(set(options)):
                    raise ValueError(f"Multi select field '{field_name}' must use valid options")
            validated[field_name] = value
        self.data = validated
