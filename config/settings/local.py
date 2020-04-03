from .base import *
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="asd485a353SD45jknjksd8989735245SDBHkjh82213SHDBoiierup",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
SITE_URL = env("SITE_URL", default="http://localhost:8008")

# django-debug-toolbar
# ------------------------------------------------------------------------------
INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS.append("django_extensions")
