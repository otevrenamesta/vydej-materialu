from django.urls import path

from .views import (
    AboutView,
    DispenseEditView,
    DispenseNewView,
    DispenseView,
    LocationView,
    LoginView,
    LogoutView,
    PasswordResetView,
    RegionListView,
    RegionView,
    RegistrationView,
)

app_name = "main"

urlpatterns = [
    path("", RegionListView.as_view(), name="region_list"),
    path("oblast/<int:id>", RegionView.as_view(), name="region"),
    path("lokalita/<int:id>", LocationView.as_view(), name="location"),
    path("o-aplikaci", AboutView.as_view(), name="about"),
    path("registrace/", RegistrationView.as_view(), name="registration"),
    path("reset-hesla/", PasswordResetView.as_view(), name="password_reset"),
    path("prihlaseni/", LoginView.as_view(), name="login"),
    path("odhlasit/", LogoutView.as_view(), name="logout"),
    path("vydej/", DispenseView.as_view(), name="dispense"),
    path(
        "vydej/novy/<int:id_card_no>/", DispenseNewView.as_view(), name="dispense_new"
    ),
    path("vydej/editace/<int:pk>/", DispenseEditView.as_view(), name="dispense_edit",),
]
