from django.conf import settings as django_settings


def settings(*args, **kwargs):
    return {"settings": django_settings}
