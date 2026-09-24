from accounts.models import Entity
from rest_framework.serializers import ModelSerializer


class EntitySerializer(ModelSerializer):
    """Entity serializer."""

    class Meta:
        model = Entity
        fields = ["id", "name", "logo_url", "parent"]
