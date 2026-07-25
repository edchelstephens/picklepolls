from django.contrib import admin

from polls.models import QuestionType


class QuestionTypeAdmin(admin.ModelAdmin):
    """QuestionType model admin."""


admin.site.register(QuestionType, QuestionTypeAdmin)
