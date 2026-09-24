from accounts.models import Entity
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class EntitySerializer(ModelSerializer):
    """Entity serializer."""

    owner = SerializerMethodField()
    admins = SerializerMethodField()

    class Meta:
        model = Entity
        fields = ["id", "name", "logo_url", "parent", "owner", "admins"]

    def get_owner(self, obj):
        """Get owner field."""
        owner_data = None

        if obj.owner is not None:
            owner_data = obj.owner.get_data()

        return owner_data

    def get_admins(self, obj):
        """Get admins field."""

        admins_data = []

        if obj.admins is not None:
            admins_data = [admin.get_data() for admin in obj.admins.all()]

        return admins_data
