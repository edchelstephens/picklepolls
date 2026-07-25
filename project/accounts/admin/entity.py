from django.contrib import admin
from accounts.models import Entity


class EntityAdmin(admin.ModelAdmin):
    """Entity model admin."""


admin.site.register(Entity, EntityAdmin)
