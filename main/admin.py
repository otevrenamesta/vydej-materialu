from django.contrib import admin

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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(admins=request.user)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    actions = None
    list_display = ("name", "region", "status")
    list_filter = ("status", "region")
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ("name", "region__name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(region__admins=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "region":
            kwargs["queryset"] = Region.objects.filter(admins=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LocationStaffInline(admin.TabularInline):
    model = LocationStaff
    extra = 1


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    actions = None
    list_display = ("name", "region", "status")
    list_filter = ("status", "region")
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ("name", "region__name")
    inlines = (LocationStaffInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(region__admins=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "region":
            kwargs["queryset"] = Region.objects.filter(admins=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
        return qs.filter(region__admins=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "material":
            if not request.user.is_superuser:
                kwargs["queryset"] = Material.objects.filter(
                    region__in=Region.objects.filter(admins=request.user)
                )
        if db_field.name == "location":
            if not request.user.is_superuser:
                kwargs["queryset"] = Location.objects.filter(
                    region__in=Region.objects.filter(admins=request.user)
                )
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
            return ("dispensed", "region", "user")
        return ("dispensed",)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ("region", "user", "date")
        return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(region__admins=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "operation":
            kwargs["choices"] = (
                choice
                for choice in MaterialRecord.OPERATION_CHOICES
                if choice[0] != MaterialRecord.DISPENSED
            )
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "material":
            if not request.user.is_superuser:
                kwargs["queryset"] = Material.objects.filter(
                    region__in=Region.objects.filter(admins=request.user)
                )
        if db_field.name == "location":
            if not request.user.is_superuser:
                kwargs["queryset"] = Location.objects.filter(
                    region__in=Region.objects.filter(admins=request.user)
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return obj.operation != MaterialRecord.DISPENSED
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return obj.operation != MaterialRecord.DISPENSED
        return super().has_delete_permission(request, obj)
