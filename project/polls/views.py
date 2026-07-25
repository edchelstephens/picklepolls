from django.db.models import F
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect


from polls.models import Question, Choice


def index(request: HttpRequest) -> HttpResponse:
    """Index page."""

    latest_question_list = Question.objects.order_by("-publication_datetime")[:5]
    context = {"latest_question_list": latest_question_list}

    return render(request, "polls/index.html", context)


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    """Question detail page."""
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "polls/detail.html", context)


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    """Question results page."""
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "polls/results.html", context)


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    """Vote view."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST["choice"]
        selected_choice = question.choice_set.get(pk=choice_id)
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
