from utils.view import LoginRequiredRestAPIView, RestAPIView
from utils.exceptions import HumanReadableError

from django.db.models import F

from polls.serializers import QuestionSerializer, ChoiceSerializer
from polls.models import Question, Choice
from accounts.models import Entity


class PublicQuestionsAPIView(RestAPIView):
    """Public api endpoint for questions."""

    def get(self, request, *args, **kwargs):
        """Get all active polls."""
        try:
            questions = Question.objects.filter(is_active=True)
            serializer = QuestionSerializer(questions, many=True)
            data = serializer.data
            response = {"data": data, "count": len(data)}
            return self.success_response(response)
        except HumanReadableError as exc:
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)


class PublicQuestionAPIView(RestAPIView):
    """Public api endpoint for question."""

    def get(self, request, pk, *args, **kwargs):
        """Handle get request."""
        try:
            if not Question.objects.filter(pk=pk).exists():
                self.raise_error(
                    title="Not Found", message="Question not found", status=404
                )

            question = Question.objects.get(pk=pk)

            response = question.get_data()

            return self.success_response(response)
        except HumanReadableError as exc:
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)


class PublicQuestionVoteAPIView(RestAPIView):
    """Public vote on a question choice."""

    def post(self, request, pk, *args, **kwargs):
        """Handle post request."""
        try:

            choice_id = request.data.get("choice")

            if not Choice.objects.filter(pk=choice_id, question__id=pk).exists():
                self.raise_error(
                    title="Not Found",
                    message="Unable to find choice for given question id.",
                    status=404,
                )

            choice = Choice.objects.get(pk=choice_id, question__id=pk)

            choice.votes = F("votes") + 1
            choice.save()

            question = choice.question
            response = {
                "title": "Success",
                "message": "Voted on question.",
                "question": question.get_data(),
            }

            return self.success_response(response)

        except HumanReadableError as exc:
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)


class QuestionAPIView(LoginRequiredRestAPIView):
    """Question api view."""

    def post(self, request, *args, **kwargs):
        """Handle post request for creation of question."""
        try:
            request_data = request.data
            user = self.get_user_instance(request)
            entity = Entity.objects.get(owner=user)

            choices = request_data["choices"]
            data = {
                "question_text": request_data["question_text"],
                "question_type": request_data["question_type"],
                "entity": entity.pk,
                "author": user.pk,
            }

            question_serializer = QuestionSerializer(data=data)
            if question_serializer.is_valid():
                question = question_serializer.save()

                choices_data = [
                    {"question": question.pk, "choice_text": choice_text}
                    for choice_text in choices
                ]

                choices_serializer = ChoiceSerializer(data=choices_data, many=True)
                if choices_serializer.is_valid():
                    choices_saved = choices_serializer.save()

                else:
                    self.raise_error(errors=choices_serializer.errors)

                response = question_serializer.data

                return self.success_response(response)
            else:
                self.raise_error(errors=question_serializer.errors)

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
