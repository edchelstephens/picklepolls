from rest_framework.serializers import ModelSerializer
from polls.models import QuestionType


class QuestionTypeSerializer(ModelSerializer):
    """Question Type serializer."""

    class Meta:
        model = QuestionType
        fields = ["id", "name"]
