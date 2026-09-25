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
    publication_datetime = models.DateTimeField(
        verbose_name="datetime published", default=timezone.now, blank=True
    )
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
        current_datetime = timezone.now()

        return (
            current_datetime - datetime.timedelta(days=1)
            <= self.publication_datetime
            <= current_datetime
        )

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
    def has_choices(self) -> bool:
        """Check if question has choices."""
        return self.choices.exists()

    @property
    def winning_choice(self) -> models.Model:
        """Get the winning choice based on vote count."""
        if not self.has_votes:
            raise ValueError("The poll question has not been voted yet.")

        return self.choices.order_by("-votes").first()

    @property
    def losing_choice(self) -> models.Model:
        """Get the losing choice based on vote count."""
        if not self.has_multiple_votes:
            raise ValueError("The poll does not have multiple choices voted yet.")

        return self.choices.order_by("-votes").last()

    def get_choices_ordered_by_winning_votes(self) -> models.QuerySet:
        """Get choices ordered by winning votes."""
        return self.choices.order_by("-votes")

    def get_choices_ordered_by_choice_text(self) -> models.QuerySet:
        """Get choices ordered by choice text."""
        return self.choices.order_by("choice_text")

    def get_data(self) -> dict:
        """Get data from object."""
        data = {
            "id": self.pk,
            "question_text": self.question_text,
            "question_type__id": (
                self.question_type.pk if self.question_type is not None else None
            ),
            "question_type_name": (
                self.question_type.name if self.question_type is not None else None
            ),
            "is_active": self.is_active,
            "entity__id": self.entity.id if self.entity is not None else None,
            "entity__name": self.entity.name if self.entity is not None else None,
            "author__id": self.author.id if self.author is not None else None,
            "author__email": self.author.email if self.author is not None else None,
            "choices": [choice.get_data() for choice in self.choices.all()],
        }

        return data
