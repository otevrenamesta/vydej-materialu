import secrets
from functools import partial

from django.conf import settings
from django.db import models

from main.models import Location

generate_token = partial(secrets.token_urlsafe, 50)


class ApiToken(models.Model):
    token = models.CharField(max_length=70, db_index=True, default=generate_token)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
