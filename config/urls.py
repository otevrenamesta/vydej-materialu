from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django_registration.backends.activation import views as reg_views

import api.urls
import main.urls
from users.forms import UserRegistrationForm

urlpatterns = [
    # api urls
    path(settings.API_URL, include(api.urls)),
    # admin urls
    path(settings.ADMIN_URL, admin.site.urls),
    # django-registration urls
    path(
        "registrace/",
        reg_views.RegistrationView.as_view(form_class=UserRegistrationForm),
        name="django_registration_register",
    ),
    path(
        "registrace/aktivace/dokoncena/",
        TemplateView.as_view(
            template_name="django_registration/activation_complete.html"
        ),
        name="django_registration_activation_complete",
    ),
    path(
        "registrace/aktivace/<str:activation_key>/",
        reg_views.ActivationView.as_view(),
        name="django_registration_activate",
    ),
    path(
        "registrace/dokoncena/",
        TemplateView.as_view(
            template_name="django_registration/registration_complete.html"
        ),
        name="django_registration_complete",
    ),
    path(
        "registrace/uzavrena/",
        TemplateView.as_view(
            template_name="django_registration/registration_disallowed.html"
        ),
        name="django_registration_disallowed",
    ),
    # main urls
    path("", include(main.urls)),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
