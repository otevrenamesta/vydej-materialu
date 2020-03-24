from django.urls import path

from .views import DispenseView, LoginView, MaterialView, ValidateView

app_name = "api"

urlpatterns = [
    path("start", LoginView.as_view(), name="login"),
    path("material", MaterialView.as_view(), name="material"),
    path("dispense", DispenseView.as_view(), name="dispense"),
    path("validate", ValidateView.as_view(), name="validate"),
]
