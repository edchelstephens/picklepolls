from utils.view import LoginRequiredRestAPIView
from utils.exceptions import HumanReadableError

from polls.serializers import QuestionSerializer
from polls.models import Question
from accounts.models import Entity


class QuestionAPIView(LoginRequiredRestAPIView):
    """Question api view."""

    def post(self, request, *args, **kwargs):
        """Handle post request for creation of question."""
        try:
            request_data = request.data
            user = self.get_user_instance(request)
            entity = Entity.objects.get(owner=user)

            data = {
                "question_text": request_data["question_text"],
                "question_type": request_data["question_type"],
                "entity": entity.pk,
                "author": user.pk,
            }

            serializer = QuestionSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()
                response = instance.get_data()
                return self.success_response(response)
            else:
                self.raise_error(errors=serializer.errors)

        except HumanReadableError as exc:
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)

    def delete(self, request, pk, *args, **kwargs):
        """Handle post request for creation of question."""
        try:
            if not Question.objects.filter(pk=pk, author=request.user).exists():
                self.raise_error(title="Not Found", message="Question does not exist")

            instance = Question.objects.get(pk=pk, author=request.user)
            instance.delete()

            response = {
                "is_success": True,
                "title": "Success",
                "message": "Question deleted.",
            }

            return self.success_response(response)
        except HumanReadableError as exc:
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)
