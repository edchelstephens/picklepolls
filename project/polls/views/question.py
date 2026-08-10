from django.utils import timezone
from django.db.models import F
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView

from polls.models import Question, Choice

from utils.view import DjangoView


class PollsIndexView(TemplateView):
    """Index view."""

    template_name = "polls/index.html"

    def get_context_data(self, **kwargs) -> dict:
        """Get context data."""

        question_list = Question.objects.filter(
            publication_datetime__lte=timezone.now()
        ).order_by("-publication_datetime")
        total_polls = Question.objects.count()
        total_votes = sum(Choice.objects.values_list("votes", flat=True))

        context = {
            "question_list": question_list,
            "has_polls": total_polls > 0,
            "total_polls": total_polls,
            "total_votes": total_votes,
        }

        return context


class PollDetailView(DetailView):
    """Poll Detail view."""

    model = Question
    template_name = "polls/detail.html"


class PollResultsView(DetailView):
    """Poll results view."""

    model = Question
    template_name = "polls/results.html"


class PollVoteView(DjangoView):
    """Poll vote view."""

    def post(self, request, pk: int, *args, **kwargs):
        """Poll vote view."""

        question = get_object_or_404(Question, pk=pk)
        try:
            choice_id = request.POST["choice"]
            selected_choice = question.choices.get(pk=choice_id)
        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
                context={
                    "question": "question",
                    "error_message": "You did not select a choice.",
                },
            )
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()

            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
