from django.contrib import admin
from django.utils.html import format_html
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    """User model admin."""

    list_display = [
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "image_preview",
        "company",
    ]

    @admin.display(description="Image Preview")
    def image_preview(self, obj):
        """Get the image preview html."""
        logo_html = ""
        if obj.has_image:

            logo_html = format_html(
                '<a href={}><img src={} style="max-height: 30px; max-width:300px" /></a>',
                obj.profile_pic_url,
                obj.profile_pic_url,
            )
        return logo_html


admin.site.register(User, UserAdmin)
