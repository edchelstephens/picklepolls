from django.urls import path

from api.views import (
    TokenAPIView,
    EntitiesAPIView,
    QuestionAPIView,
    PublicQuestionTypesAPIView,
    PublicQuestionsAPIView,
    PublicQuestionAPIView,
    PublicQuestionVoteAPIView,
    PublicChoicesAPIView,
    PublicEntitiesAPIView,
)

app_name = "api"

urlpatterns = [
    path("accounts/login/", TokenAPIView.as_view()),
    path("accounts/entities/", EntitiesAPIView.as_view()),
    path("polls/question/", QuestionAPIView.as_view()),
    path("polls/question/<int:pk>/", QuestionAPIView.as_view()),
    path("public/entities/", PublicEntitiesAPIView.as_view()),
    path("public/question_types/", PublicQuestionTypesAPIView.as_view()),
    path("public/choices/", PublicChoicesAPIView.as_view()),
    path("public/questions/", PublicQuestionsAPIView.as_view()),
    path("public/question/<int:pk>/", PublicQuestionAPIView.as_view()),
    path("public/question/<int:pk>/vote/", PublicQuestionVoteAPIView.as_view()),
]
