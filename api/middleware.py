import re

from django.conf import settings
from django.http import JsonResponse

from .models import ApiToken


class ApiTokenAuthMiddleware:
    """
    Custom authentication middleware using token.

    Token can be passed in Authorization HTTP header or as URL parameter.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path_info.startswith(f"/{settings.API_URL}"):
            return self.get_response(request)

        token = None

        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header is not None:
            m = re.match(r"Bearer (?P<token>.+)", auth_header)
            if m:
                token = m.group("token")
            else:
                body = {
                    "result": "error",
                    "code": "invalid-request",
                    "message": 'Špatná autentifikační HTTP hlavička. Očekává se: "Bearer <token>"',
                }
                return JsonResponse(body, status=400)
        else:
            token = request.GET.get("token")

        if token is not None:
            try:
                api_token = ApiToken.objects.select_related("user", "location").get(
                    token=token
                )
                request.user = api_token.user
                request.user.api_location = api_token.location
            except ApiToken.DoesNotExist:
                body = {
                    "result": "error",
                    "code": "invalid-token",
                    "message": "Problém s ověřením identity. Kontaktujte koordinátora.",
                }
                return JsonResponse(body, status=401)

        return self.get_response(request)
