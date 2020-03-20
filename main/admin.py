from django.contrib import admin

from .models import Dispensed, Location, LocationStaff, Material, MaterialRecord, Region
from .models import RegionAdmin as RegionAdminModel

admin.site.site_header = "Administrace výdeje materiálu"
admin.site.site_title = "Administrace výdeje materiálu"


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
    pass


@admin.register(MaterialRecord)
class MaterialRecordAdmin(admin.ModelAdmin):
    pass
