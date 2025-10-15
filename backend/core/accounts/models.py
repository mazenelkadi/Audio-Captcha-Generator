from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    MASTER = "master", "Master"
    MASTER_EDITOR = "master_editor", "Master Editor"
    MASTER_VIEWER = "master_viewer", "Master Viewer"
    ADMIN = "admin", "Admin"
    VIEWER = "viewer", "Viewer"


class User(AbstractUser):
    role = models.CharField(
        max_length=32,
        choices=Roles.choices,
        default=Roles.VIEWER,
        help_text="Determines the global permission level of the user.",
    )

    def is_master(self) -> bool:
        return self.role in {Roles.MASTER, Roles.MASTER_EDITOR, Roles.MASTER_VIEWER}

    @property
    def can_edit_any_base(self) -> bool:
        return self.role in {Roles.MASTER, Roles.MASTER_EDITOR}

    @property
    def can_delete_bases(self) -> bool:
        return self.role == Roles.MASTER

    @property
    def can_create_bases(self) -> bool:
        return self.role in {Roles.MASTER, Roles.MASTER_EDITOR}

    def __str__(self) -> str:  # pragma: no cover - repr helper
        return f"{self.username} ({self.get_role_display()})"
