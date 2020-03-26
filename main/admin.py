from django.contrib import admin
from django.db import models
from django.db.models import Q
from pagedown.widgets import AdminPagedownWidget

from .forms import LocationAdminForm
from .models import Dispensed, Location, LocationStaff, Material, MaterialRecord, Region
from .models import RegionAdmin as RegionAdminModel

admin.site.site_header = "Správa výdeje materiálu"
admin.site.site_title = "Správa výdeje materiálu"
admin.site.index_title = "Správa výdeje materiálu"


class RegionAdminInline(admin.TabularInline):
    model = RegionAdminModel
    extra = 1


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    actions = None
    list_display = ("name", "status")
    list_filter = ("status",)
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ("name",)
    inlines = (RegionAdminInline,)
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(admins=request.user)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    actions = None
    list_display = ("name", "region", "status", "limit", "period")
    list_filter = ("status", "region")
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ("name", "region__name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(region__admins=request.user) | Q(region__location__staff=request.user)
        ).distinct()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "region":
            kwargs["queryset"] = Region.objects.filter(admins=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LocationStaffInline(admin.TabularInline):
    model = LocationStaff
    extra = 1
    radio_fields = {"status": admin.HORIZONTAL}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    form = LocationAdminForm
    actions = None
    list_display = ("id", "name", "region", "status")
    list_display_links = ("id", "name")
    list_filter = ("status", "region")
    fields = ("id", "name", "region", "status", "about", "address", "phone")
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ("name", "region__name")
    inlines = (LocationStaffInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(region__admins=request.user) | Q(staff=request.user)
        ).distinct()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "region":
            kwargs["queryset"] = Region.objects.filter(admins=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and not (
            request.user.is_superuser or request.user.is_region_admin
        ):
            return ("id", "region")
        return ("id",)


@admin.register(Dispensed)
class DispensedAdmin(admin.ModelAdmin):
    actions = None
    list_display = (
        "id_card_no",
        "material",
        "location",
        "quantity",
        "created",
    )
    list_filter = ("material", "region", "location")
    search_fields = ("id_card_no", "material__name", "location__name", "region__name")

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ("region", "user", "created", "changed")
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ("region", "user", "created", "changed")
        return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(region__admins=request.user) | Q(location__staff=request.user)
        ).distinct()

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "material":
            if not request.user.is_superuser:
                kwargs["queryset"] = Material.objects.filter(
                    Q(region__admins=request.user)
                    | Q(region__location__staff=request.user)
                ).distinct()
        if db_field.name == "location":
            if not request.user.is_superuser:
                kwargs["queryset"] = Location.objects.filter(
                    Q(region__admins=request.user) | Q(staff=request.user)
                ).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MaterialRecord)
class MaterialRecordAdmin(admin.ModelAdmin):
    actions = None
    list_display = ("material", "location", "quantity", "operation", "date")
    list_filter = ("operation", "material", "region", "location")
    search_fields = ("material__name", "location__name", "region__name")
    radio_fields = {"operation": admin.HORIZONTAL}

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ("region", "user")
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ("region", "user", "date")
        return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(region__admins=request.user) | Q(location__staff=request.user)
        ).distinct()

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "material":
            if not request.user.is_superuser:
                kwargs["queryset"] = Material.objects.filter(
                    Q(region__admins=request.user)
                    | Q(region__location__staff=request.user)
                ).distinct()
        if db_field.name == "location":
            if not request.user.is_superuser:
                kwargs["queryset"] = Location.objects.filter(
                    Q(region__admins=request.user) | Q(staff=request.user)
                ).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
