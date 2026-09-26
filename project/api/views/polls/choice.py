from utils.exceptions import HumanReadableError
from utils.view import RestAPIView

from polls.serializers import ChoiceSerializer
from polls.models import Choice


class PublicChoicesAPIView(RestAPIView):
    """Public api endpoint for choices."""

    def get(self, request, *args, **kwargs):
        """Get all choices from all active questions."""
        try:
            choices = Choice.objects.filter(question__is_active=True)
            serializer = ChoiceSerializer(choices, many=True)

            data = serializer.data

            response = {"data": data, "count": len(data)}
            return self.success_response(response)
        except HumanReadableError as exc:
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)
