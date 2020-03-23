from django.urls import path

from .views import LoginView

app_name = "api"

urlpatterns = [
    path("start", LoginView.as_view(), name="login"),
]
