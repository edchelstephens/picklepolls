from django.urls import path

from polls import views

app_name = "polls"

urlpatterns = [
    path("", views.PollsIndexView.as_view(), name="index"),
    path("<int:pk>/", views.PollDetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.PollResultsView.as_view(), name="results"),
    path("<int:pk>/vote/", views.PollVoteView.as_view(), name="vote"),
]
