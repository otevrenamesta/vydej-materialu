from django.urls import path

from .views import (
    DispenseEditView,
    DispenseNewView,
    DispenseView,
    HomeView,
    LoginView,
    LogoutView,
    PasswordResetView,
    RegistrationView,
)

app_name = "main"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("registrace/", RegistrationView.as_view(), name="registration"),
    path("reset-hesla/", PasswordResetView.as_view(), name="password_reset"),
    path("prihlaseni/", LoginView.as_view(), name="login"),
    path("odhlasit/", LogoutView.as_view(), name="logout"),
    path("vydej/", DispenseView.as_view(), name="dispense"),
    path(
        "vydej/novy/<int:id_card_no>/", DispenseNewView.as_view(), name="dispense_new"
    ),
    path("vydej/editace/<int:pk>/", DispenseEditView.as_view(), name="dispense_edit"),
]
