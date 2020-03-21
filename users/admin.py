from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    actions = None
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "status",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "status",
        "is_staff",
        "is_superuser",
    )
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ("username", "first_name", "last_name", "email")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "email",
                    "first_name",
                    "last_name",
                    "phone",
                    "status",
                )
            },
        ),
        (
            "Podrobnosti",
            {
                "classes": ("collapse",),
                "fields": ("is_active", "is_staff", "is_superuser", "groups"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ("is_active", "is_staff", "groups")
        return ("is_active", "is_staff", "groups", "is_superuser")
