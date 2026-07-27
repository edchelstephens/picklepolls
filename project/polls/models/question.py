import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question model."""

    question_text = models.CharField(max_length=200)
    question_type = models.ForeignKey(
        to="polls.QuestionType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions",
    )
    publication_datetime = models.DateTimeField(verbose_name="datetime published")
    is_active = models.BooleanField(default=True)
    entity = models.ForeignKey(
        to="accounts.Entity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions_asked",
    )
    author = models.ForeignKey(
        to="accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions_authored",
    )

    def __repr__(self) -> str:
        """Machine-readable representation of the model instance."""
        return f"Question(pk={self.pk}, question_text={self.question_text}, publication_datetime={self.publication_datetime})"

    def __str__(self) -> str:
        """Human-readable representation of the model instance."""
        return self.question_text

    def was_published_recently(self) -> bool:
        """Check if question was published recently."""
        return self.publication_datetime >= timezone.now() - datetime.timedelta(days=1)

    @property
    def total_choices(self) -> int:
        """Get total choices count."""
        return self.choices.count()

    @property
    def total_votes(self) -> int:
        """Get total votes on all choices under question."""
        votes = self.choices.values_list("votes", flat=True)
        return sum(votes)

    @property
    def has_votes(self) -> bool:
        """Check if question choices has votes already."""
        return self.choices.filter(votes__gt=0).exists()

    @property
    def has_multiple_votes(self) -> bool:
        """Check if the question has at least 2 choices with votes."""
        choices_with_votes_count = self.choices.filter(votes__gt=0).count()
        return choices_with_votes_count > 1

    @property
    def winning_choice(self) -> models.Model:
        """Get the winning choice based on vote count."""
        if not self.has_votes:
            raise ValueError("The poll question has not been voted yet.")

        return self.choices.order_by("votes").last()

    @property
    def losing_choice(self) -> models.Model:
        """Get the losing choice based on vote count."""
        if not self.has_multiple_votes:
            raise ValueError("The poll does not have multiple choices voted yet.")

        return self.choices.order_by("votes").first()
