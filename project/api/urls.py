from django.urls import path

from api.views import TokenAPIView

app_name = "api"

urlpatterns = [path("login/", TokenAPIView.as_view())]
