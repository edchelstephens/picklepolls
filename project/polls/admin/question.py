from django.contrib import admin

from polls.models import Question, Choice


class ChoiceInLine(admin.StackedInline):
    """Choice in line"""

    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    """Question model admin."""

    list_display = [
        "question_text",
        "total_choices",
        "total_votes",
        "publication_datetime",
        "published_recently",
    ]
    list_filter = ["publication_datetime"]

    inlines = [ChoiceInLine]

    @admin.display(description="Total Choices")
    def total_choices(self, obj):
        """Return the total choices count of the question."""
        return obj.choices.count()

    @admin.display(description="Total Votes")
    def total_votes(self, obj):
        """Return the total votes count of all the choices for the question."""

        choices_votes = obj.choices.values_list("votes", flat=True)
        return sum(choices_votes)

    @admin.display(boolean=True, description="Published Recently?")
    def published_recently(self, obj):
        """Return True if the question was published recently."""
        return obj.was_published_recently()


admin.site.register(Question, QuestionAdmin)
