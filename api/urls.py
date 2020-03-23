from django.urls import path

from .views import LoginView, MaterialView

app_name = "api"

urlpatterns = [
    path("start", LoginView.as_view(), name="login"),
    path("material", MaterialView.as_view(), name="material"),
]
