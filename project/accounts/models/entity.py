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

    owner = models.ForeignKey(
        to="accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entities_owned",
    )

    admins = models.ManyToManyField(
        to="accounts.User", blank=True, related_name="entities_admined"
    )

    def __repr__(self) -> str:
        """Machine readable string representation of the instance."""
        return f"Entity(pk={self.pk}, name={self.name})"

    def __str__(self) -> str:
        """Human readable string representation of the instance."""
        return self.name

    @property
    def has_image(self) -> bool:
        """Check if logo url is filled."""
        return len(self.logo_url) > 4

    def get_data(self) -> dict:
        """Get data."""
        data = {"id": self.pk, "name": self.name, "logo_url": self.logo_url}

        return data
