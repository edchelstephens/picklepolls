from polls.serializers import QuestionTypeSerializer
from polls.models import QuestionType


from utils.view import RestAPIView
from utils.exceptions import HumanReadableError


class PublicQuestionTypesAPIView(RestAPIView):
    """Question types api view."""

    def get(self, request, *args, **kwargs):
        """Handle get request."""
        try:
            queryset = QuestionType.objects.all()
            serializer = QuestionTypeSerializer(instance=queryset, many=True)
            data = serializer.data

            response = {"data": data, "count": len(data)}
            return self.success_response(response)
        except HumanReadableError as exc: # pragma no cover
            return self.error_response(exc)
        except Exception as exc: # pragma no cover
            return self.server_error_response(exc)
