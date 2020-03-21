from django.contrib.auth.models import Group

from .config import LOCATION_ADMIN, LOCATION_VOLUNTEER, REGION_ADMIN


def setup_user_permissons(user):
    """
    Sets user's groups and is_staff flag based on RegionAdmin and LocationStaff
    membership.
    """
    groups = Group.objects.all()
    region_admin = next(g for g in groups if g.name == REGION_ADMIN["group_name"])
    location_admin = next(g for g in groups if g.name == LOCATION_ADMIN["group_name"])
    location_volunteer = next(
        g for g in groups if g.name == LOCATION_VOLUNTEER["group_name"]
    )

    if user.is_region_admin:
        user.groups.add(region_admin)
    else:
        user.groups.remove(region_admin)

    if user.is_location_admin:
        user.groups.add(location_admin)
    else:
        user.groups.remove(location_admin)

    if user.is_location_volunteer:
        user.groups.add(location_volunteer)
    else:
        user.groups.remove(location_volunteer)

    if (
        user.is_superuser
        or user.is_region_admin
        or user.is_location_admin
        or user.is_location_volunteer
    ):
        user.is_staff = True
    else:
        user.is_staff = False
    user.save()
