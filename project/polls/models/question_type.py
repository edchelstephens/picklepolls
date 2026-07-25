from django.db import models


class QuestionType(models.Model):
    """Question Type model."""

    name = models.CharField(max_length=200)

    def __repr__(self) -> str:
        """Machine readable string representation of the instance."""
        return f"QuestionType(pk={self.pk}, question_type={self.name})"

    def __str__(self) -> str:
        """Human readable string representation of the instance"""
        return self.name
