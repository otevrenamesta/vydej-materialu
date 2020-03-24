import json

import jsonschema
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


class ApiRequestValidationMixin:
    """
    Mixin checking that the request body is a valid JSON conforming to
    a defined JSON schema. Passes on the `body` keyword argument.
    The schema is expected to be found in the `request_schema` property.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.method != "POST":
            return super().dispatch(request, *args, **kwargs)

        try:
            body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            response = {
                "result": "error",
                "code": "invalid-request",
                "message": "Nelze přečíst payload requestu.",
            }
            return JsonResponse(response, status=400)

        try:
            jsonschema.validate(body, self.request_schema)
        except jsonschema.ValidationError as err:
            path = "/".join([str(pc) for pc in err.absolute_path])
            response = {
                "result": "error",
                "code": "invalid-request",
                "message": f"/{path}: {err.message}",
            }
            return JsonResponse(response, status=400)

        return super().dispatch(request, *args, body=body, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(ApiRequestValidationMixin, View):
    request_schema = {
        "type": "object",
        "properties": {
            "login": {"type": "string"},
            "password": {"type": "string"},
            "location": {
                "oneOf": [
                    {"type": "integer", "minimum": 0},
                    {"type": "string", "regex": "^[0-9]+$"},
                ],
            },
        },
        "required": ["login", "password", "location"],
    }

    def post(self, request, body, *args, **kwargs):
        user = authenticate(username=body["login"], password=body["password"])
        if user is None:
            response = {
                "result": "error",
                "code": "invalid-credentials",
                "message": "Přihlášení se nezdařilo, nezadali jste chybné heslo?",
            }
            return JsonResponse(response, status=401)

        try:
            location = Location.objects.get(id=int(body["location"]))
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
class DispenseView(ApiStaffRequiredMixin, ApiRequestValidationMixin, View):
    request_schema = {
        "type": "object",
        "properties": {
            "idcardno": {
                "oneOf": [
                    {"type": "integer", "minimum": 0},
                    {"type": "string", "regex": "^[0-9]+$"},
                ],
            },
            "material": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "minimum": 0},
                        "quantity": {"type": "integer", "minimum": 0},
                    },
                    "required": ["id", "quantity"],
                },
            },
        },
        "required": ["idcardno"],
    }

    def post(self, request, body, *args, **kwargs):
        id_card_no = int(body["idcardno"])

        total = sum([item["quantity"] for item in body.get("material", [])])
        if total <= 0:
            response = {
                "result": "error",
                "code": "invalid-request",
                "message": "Množství materiálu musí být větší než 0.",
            }
            return JsonResponse(response, status=400)

        for item in body.get("material", []):
            try:
                material = Material.objects.get(
                    id=item["id"],
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

            Dispensed.objects.create(
                material=material,
                user=request.user,
                location=request.user.api_location,
                quantity=item["quantity"],
                id_card_no=id_card_no,
            )

        response = {"result": "success"}
        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class ValidateView(ApiStaffRequiredMixin, ApiRequestValidationMixin, View):
    request_schema = {
        "type": "object",
        "properties": {
            "idcardno": {
                "oneOf": [
                    {"type": "integer", "minimum": 0},
                    {"type": "string", "regex": "^[0-9]+$"},
                ],
            },
        },
        "required": ["idcardno"],
    }

    def post(self, request, body, *args, **kwargs):
        materials = Material.get_available(location=request.user.api_location)

        # TODO: Check that the ID is not blacklisted or stolen.
        id_card_no = int(body["idcardno"])

        # TODO: Adjust limits according to the specification.

        response = {
            "result": "success",
            "message": "V pořádku.",
            "limits": [{"id": m.id, "limit": m.limit} for m in materials],
        }
        return JsonResponse(response)
