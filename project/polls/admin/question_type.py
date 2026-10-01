from django.contrib import admin

from polls.models import QuestionType


class QuestionTypeAdmin(admin.ModelAdmin):
    """QuestionType model admin."""

    list_display = ["id", "name"]


admin.site.register(QuestionType, QuestionTypeAdmin)
