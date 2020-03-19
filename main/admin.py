from django.contrib import admin

from .models import Dispensed, Location, LocationStaff, Material, MaterialRecord, Region
from .models import RegionAdmin as RegionAdminModel


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


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    actions = None
    list_display = ("name", "region", "status")
    list_filter = ("status", "region")
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ("name", "region__name")


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


@admin.register(Dispensed)
class DispensedAdmin(admin.ModelAdmin):
    pass


@admin.register(MaterialRecord)
class MaterialRecordAdmin(admin.ModelAdmin):
    pass
