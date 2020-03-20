from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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
