from django.db import models


class Choice(models.Model):
    """Question answer choice model."""

    question = models.ForeignKey(
        to="polls.Question", on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def __repr__(self):
        """Machine-readable representation of the model instance."""
        return f"Choice(pk={self.pk}, question_id={self.question.pk}, choice_text={self.choice_text}, votes={self.votes})"

    def __str__(self):
        """Human-readable representation of the model instance."""
        return (
            f"{self.question.question_text} - {self.choice_text} - {self.votes} votes"
        )

    @property
    def vote_percentage(self) -> float:
        """Get the percentage of this choice from the total casted votes across all choices under question."""
        total_votes = self.question.total_votes
        percentage = round((self.votes / total_votes) * 100)

        return percentage
