from django.contrib import admin
from django.utils.html import format_html
from accounts.models import Entity


class EntityAdmin(admin.ModelAdmin):
    """Entity model admin."""

    list_display = [
        "id",
        "name",
        "parent",
        "image_preview",
    ]

    @admin.display(description="Image Preview")
    def image_preview(self, obj):
        """Get the image preview html."""
        logo_html = ""
        if obj.has_image:

            logo_html = format_html(
                '<a href={}><img src={} style="max-height: 30px; max-width:300px" /></a>',
                obj.logo_url,
                obj.logo_url,
            )
        return logo_html


admin.site.register(Entity, EntityAdmin)
