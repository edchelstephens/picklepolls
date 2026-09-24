from django.urls import path

from api.views import TokenAPIView, EntitiesAPIView

app_name = "api"

urlpatterns = [
    path("accounts/login/", TokenAPIView.as_view()),
    path("accounts/entities/", EntitiesAPIView.as_view()),
]
