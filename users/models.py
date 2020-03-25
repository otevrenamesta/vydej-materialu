from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import LocationStaff


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Uživatel musí mít email.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    PENDING = "pending"
    ACTIVE = "active"
    DISABLED = "disabled"
    STATUS_CHOICES = [
        (PENDING, "čekatel"),
        (ACTIVE, "aktivní"),
        (DISABLED, "blokován"),
    ]

    # remove username field as we are using email instead
    username = None
    # override email field with required and unique one
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField("telefon", max_length=20, null=True, blank=True)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=PENDING, db_index=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["email"]
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.status == self.ACTIVE:
            self.is_active = True
        elif self.status == self.DISABLED:
            self.is_active = False
        if self.is_superuser:
            self.is_staff = True
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
