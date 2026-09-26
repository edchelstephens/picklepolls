from rest_framework.serializers import ModelSerializer
from polls.models import Choice


class ChoiceSerializer(ModelSerializer):
    """Choice serializer."""

    class Meta:
        model = Choice
        fields = ["id", "question", "choice_text", "votes"]
