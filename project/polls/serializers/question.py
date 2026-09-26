from rest_framework.serializers import ModelSerializer
from polls.models import Question


class QuestionSerializer(ModelSerializer):
    """Question serializer."""

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "question_type",
            "entity",
        ]
