import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import ApiToken
from main.models import Location, LocationStaff


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            response = {
                "result": "error",
                "code": "invalid-request",
                "message": "Nelze přečíst payload requestu.",
            }
            return JsonResponse(response, status=400)

        user = authenticate(username=body.get("login"), password=body.get("password"))
        if user is None:
            response = {
                "result": "error",
                "code": "invalid-credentials",
                "message": "Přihlášení se nezdařilo, nezadali jste chybné heslo?",
            }
            return JsonResponse(response, status=401)

        try:
            location = Location.objects.get(id=int(body.get("location")))
        except Location.DoesNotExist:
            response = {
                "result": "error",
                "code": "invalid-location",
                "message": "Taková lokalita neexistuje. Kontaktujte koordinátora.",
            }
            return JsonResponse(response, status=404)

        if not LocationStaff.is_assigned(user, location):
            response = {
                "result": "error",
                "code": "invalid-location",
                "message": "Nejte přiřazen(a) k lokalitě. Kontaktujte koordinátora.",
            }
            return JsonResponse(response, status=401)

        token = ApiToken.objects.create(user=user, location=location)
        response = {"result": "success", "token": token.token}
        return JsonResponse(response)
