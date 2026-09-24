from accounts.models import Entity
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class EntitySerializer(ModelSerializer):
    """Entity serializer."""

    owner = SerializerMethodField()

    class Meta:
        model = Entity
        fields = ["id", "name", "logo_url", "parent", "owner"]

    def get_owner(self, obj):
        """Get owner field."""
        owner_data = None

        if obj.owner is not None:
            owner_data = obj.owner.get_data()

        return owner_data
