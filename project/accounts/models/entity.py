from django.db import models


class Entity(models.Model):
    """Entity model. An entity is generally any entity, a company, a club, an organization."""

    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    logo_url = models.URLField(blank=True)

    def __repr__(self) -> str:
        """Machine readable string representation of the instance."""
        return f"Entity(pk={self.pk}, name={self.name})"

    def __str__(self) -> str:
        """Human readable string representation of the instance."""
        return self.name
