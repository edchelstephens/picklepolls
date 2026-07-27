from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model."""

    profile_pic_url = models.URLField(blank=True)
    company = models.ForeignKey(
        to="accounts.Entity", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __repr__(self) -> str:
        """Machine readable string representation of the instance."""
        return f"User(pk={self.pk}, email={self.email})"

    def __str__(self) -> str:
        """Human readable string representation of the instance."""
        return f"{self.first_name} {self.last_name}"

    @property
    def has_image(self) -> bool:
        """Check if has profile pic url."""
        return len(self.profile_pic_url) > 4
