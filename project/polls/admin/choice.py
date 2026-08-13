from django.contrib import admin

from polls.models import Choice


class ChoiceAdmin(admin.ModelAdmin):
    """Choice model admin."""

    list_display = ["question__question_text", "choice_text", "votes"]
    list_filter = ["question__entity", "question__is_active"]
    search_fields = ["question__question_text", "choice_text"]


admin.site.register(Choice, ChoiceAdmin)
