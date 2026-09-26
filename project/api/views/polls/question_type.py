from polls.serializers import QuestionTypeSerializer
from polls.models import QuestionType


from utils.view import LoginRequiredRestAPIView
from utils.exceptions import HumanReadableError


class QuestionTypesAPIView(LoginRequiredRestAPIView):
    """Question types api view."""

    def get(self, request, *args, **kwargs):
        """Handle get request."""
        try:
            queryset = QuestionType.objects.all()
            serializer = QuestionTypeSerializer(instance=queryset, many=True)
            data = serializer.data

            response = {"data": data, "count": len(data)}
            return self.success_response(response)
        except HumanReadableError as exc:
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)
