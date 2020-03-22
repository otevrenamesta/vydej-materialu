from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import LocationStaff


class User(AbstractUser):
    PENDING = "pending"
    ACTIVE = "active"
    DISABLED = "disabled"
    STATUS_CHOICES = [
        (PENDING, "čekatel"),
        (ACTIVE, "aktivní"),
        (DISABLED, "blokován"),
    ]

    phone = models.CharField("telefon", max_length=20, null=True, blank=True)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=PENDING, db_index=True
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"

    def save(self, *args, **kwargs):
        if self.status == self.ACTIVE:
            self.is_active = True
        elif self.status == self.DISABLED:
            self.is_active = False
        super().save(*args, **kwargs)

    @property
    def is_region_admin(self):
        if not hasattr(self, "_is_region_admin"):
            self._is_region_admin = self.region_set.count() > 0
        return self._is_region_admin

    @property
    def is_location_admin(self):
        if not hasattr(self, "_is_location_admin"):
            self._is_location_admin = (
                self.location_set.filter(
                    locationstaff__status=LocationStaff.ADMIN
                ).count()
                > 0
            )
        return self._is_location_admin

    @property
    def is_location_volunteer(self):
        if not hasattr(self, "_is_location_volunteer"):
            self._is_location_volunteer = (
                self.location_set.filter(
                    locationstaff__status=LocationStaff.VOLUNTEER
                ).count()
                > 0
            )
        return self._is_location_volunteer

    @property
    def api_location(self):
        """
        Location selected for API usage. Value is set in API authentication
        middleware based on ApiToken.
        """
        return getattr(self, "_api_location", None)

    @api_location.setter
    def api_location(self, location):
        self._api_location = location
