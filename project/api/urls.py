from django.urls import path

from api.views import (
    TokenAPIView,
    EntitiesAPIView,
    QuestionTypesAPIView,
    QuestionAPIView,
)

app_name = "api"

urlpatterns = [
    path("accounts/login/", TokenAPIView.as_view()),
    path("accounts/entities/", EntitiesAPIView.as_view()),
    path("polls/question_types/", QuestionTypesAPIView.as_view()),
    path("polls/question/", QuestionAPIView.as_view()),
    path("polls/question/<int:pk>/", QuestionAPIView.as_view()),
]
