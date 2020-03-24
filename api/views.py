import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import ApiToken
from main.models import Dispensed, Location, LocationStaff, Material, MaterialRecord


class ApiStaffRequiredMixin:
    """
    Mixin checking if API user is authenticated and has location which he is
    assigned to.
    """

    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or request.user.api_location is None
            or not LocationStaff.is_assigned(request.user, request.user.api_location)
        ):
            response = {
                "result": "error",
                "code": "invalid-token",
                "message": "Problém s ověřením identity. Kontaktujte koordinátora.",
            }
            return JsonResponse(response, status=401)

        return super().dispatch(request, *args, **kwargs)


def invalid_body_response():
    response = {
        "result": "error",
        "code": "invalid-request",
        "message": "Nelze přečíst payload requestu.",
    }
    return JsonResponse(response, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return invalid_body_response()

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
                "message": "Nejste přiřazen(a) k lokalitě. Kontaktujte koordinátora.",
            }
            return JsonResponse(response, status=401)

        token = ApiToken.objects.create(user=user, location=location)
        response = {"result": "success", "token": token.token}
        return JsonResponse(response)


class MaterialView(ApiStaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        materials = Material.get_available(location=request.user.api_location)

        response = {
            "result": "success",
            "material": [{"id": m.id, "name": m.name} for m in materials],
        }
        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class DispenseView(ApiStaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return invalid_body_response()

        id_card_no = body.get("idcardno")
        if not id_card_no:
            response = {
                "result": "error",
                "code": "invalid-request",
                "message": "Chybí číslo průkazu.",
            }
            return JsonResponse(response, status=400)

        for item in body.get("material", []):
            try:
                material = Material.objects.get(
                    id=int(item.get("id", 0)),
                    materialrecord__location=request.user.api_location,
                    materialrecord__operation=MaterialRecord.RECEIVED,
                )
            except Material.DoesNotExist:
                response = {
                    "result": "error",
                    "code": "invalid-request",
                    "message": "Špatné ID materiálu nebo materiál není v lokalitě dostupný.",
                }
                return JsonResponse(response, status=400)

            quantity = int(item.get("quantity", 0))
            if quantity <= 0:
                response = {
                    "result": "error",
                    "code": "invalid-request",
                    "message": "Množství materiálu musí být větší než 0.",
                }
                return JsonResponse(response, status=400)

            Dispensed.objects.create(
                material=material,
                user=request.user,
                location=request.user.api_location,
                quantity=quantity,
                id_card_no=id_card_no,
            )

        response = {"result": "success"}
        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class ValidateView(ApiStaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return invalid_body_response()

        materials = Material.get_available(location=request.user.api_location)

        response = {
            "result": "success",
            "message": "V pořádku.",
            "limits": [{"id": m.id, "limit": m.limit} for m in materials],
        }
        return JsonResponse(response)
