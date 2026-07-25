from django.contrib import admin

from polls.models import Choice


class ChoiceAdmin(admin.ModelAdmin):
    """Choice model admin."""

    list_display = ["question__question_text", "choice_text", "votes"]


admin.site.register(Choice, ChoiceAdmin)
