from django.contrib.auth.models import AbstractUser
from django.db import models


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
