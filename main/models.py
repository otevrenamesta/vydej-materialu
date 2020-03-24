from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from .utils import setup_user_permissons


class Region(models.Model):
    ACTIVE = "active"
    DISABLED = "disabled"
    STATUS_CHOICES = [
        (ACTIVE, "aktivní"),
        (DISABLED, "pozastaveno"),
    ]

    name = models.CharField("název", max_length=1000, unique=True)
    about = models.TextField("popis", null=True, blank=True)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=ACTIVE, db_index=True
    )
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name="správce", through="RegionAdmin",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Oblast"
        verbose_name_plural = "Oblasti"

    def __str__(self):
        return self.name


class RegionAdmin(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="uživatel", on_delete=models.CASCADE
    )
    region = models.ForeignKey(Region, verbose_name="oblast", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Správce oblasti"
        verbose_name_plural = "Správci oblasti"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        setup_user_permissons(self.user)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        setup_user_permissons(self.user)


class Material(models.Model):
    ACTIVE = "active"
    DISABLED = "disabled"
    STATUS_CHOICES = [
        (ACTIVE, "k dispozici"),
        (DISABLED, "blokován"),
    ]

    name = models.CharField("název", max_length=1000)
    region = models.ForeignKey(Region, verbose_name="oblast", on_delete=models.PROTECT)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=ACTIVE, db_index=True
    )
    limit = models.FloatField("limit výdeje", null=True, blank=True)
    period = models.PositiveIntegerField("perioda výdeje", null=True, blank=True)

    class Meta:
        ordering = ["name", "region"]
        verbose_name = "Materiál"
        verbose_name_plural = "Materiály"

    def __str__(self):
        return f"{self.name} ({self.region})"

    @classmethod
    def get_available(cls, location):
        return cls.objects.filter(
            materialrecord__location=location,
            materialrecord__operation=MaterialRecord.RECEIVED,
        )


class Location(models.Model):
    ACTIVE = "active"
    DISABLED = "disabled"
    STATUS_CHOICES = [
        (ACTIVE, "aktivní"),
        (DISABLED, "pozastavena"),
    ]

    name = models.CharField("název", max_length=1000)
    region = models.ForeignKey(Region, verbose_name="oblast", on_delete=models.PROTECT)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=ACTIVE, db_index=True
    )
    about = models.TextField("popis", null=True, blank=True)
    address = models.TextField("adresa", null=True, blank=True)
    phone = models.CharField("telefon", max_length=20, null=True, blank=True)
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name="personál", through="LocationStaff",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Lokalita"
        verbose_name_plural = "Lokality"

    def __str__(self):
        return f"{self.id} - {self.name} ({self.region})"


class LocationStaff(models.Model):
    PENDING = "pending"
    ADMIN = "admin"
    VOLUNTEER = "volunteer"
    STATUS_CHOICES = [
        (PENDING, "čekatel"),
        (ADMIN, "koordinátor"),
        (VOLUNTEER, "dobrovolník"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="uživatel", on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location, verbose_name="lokalita", on_delete=models.CASCADE
    )
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=PENDING
    )

    class Meta:
        ordering = ["location", "user"]
        verbose_name = "Personál lokality"
        verbose_name_plural = "Personál lokality"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        setup_user_permissons(self.user)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        setup_user_permissons(self.user)

    @classmethod
    def is_assigned(cls, user, location):
        return (
            cls.objects.filter(user=user, location=location)
            .exclude(status=LocationStaff.PENDING)
            .exists()
        )


class Dispensed(models.Model):
    material = models.ForeignKey(
        Material, verbose_name="materiál", on_delete=models.PROTECT
    )
    location = models.ForeignKey(
        Location, verbose_name="lokalita", on_delete=models.PROTECT
    )
    region = models.ForeignKey(Region, verbose_name="oblast", on_delete=models.PROTECT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="uživatel", on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField("množství")
    created = models.DateTimeField("vytvořeno", auto_now_add=True)
    changed = models.DateTimeField("upraveno", auto_now=True)
    id_card_no = models.BigIntegerField("číslo průkazu", db_index=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Výdej"
        verbose_name_plural = "Výdeje"

    def clean(self):
        if self.material.region_id != self.location.region_id:
            raise ValidationError("Nesouhlasí oblast materiálu a lokality.")

    def save(self, *args, **kwargs):
        self.region = self.location.region
        super().save(*args, **kwargs)


class MaterialRecord(models.Model):
    RECEIVED = "received"
    RETURNED = "returned"
    DISPENSED = "dispensed"
    OPERATION_CHOICES = [
        (RECEIVED, "přijetí"),
        (RETURNED, "vrácení"),
        (DISPENSED, "výdej"),
    ]

    material = models.ForeignKey(
        Material, verbose_name="materiál", on_delete=models.PROTECT
    )
    location = models.ForeignKey(
        Location, verbose_name="lokalita", on_delete=models.PROTECT
    )
    region = models.ForeignKey(Region, verbose_name="oblast", on_delete=models.PROTECT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="uživatel", on_delete=models.PROTECT
    )
    quantity = models.IntegerField("množství")
    date = models.DateTimeField("datum", auto_now_add=True)
    operation = models.CharField(
        "operace", max_length=10, choices=OPERATION_CHOICES, db_index=True
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "Záznam pohybu materiálu"
        verbose_name_plural = "Záznamy pohybů materiálů"

    def clean(self):
        if self.material.region_id != self.location.region_id:
            raise ValidationError("Nesouhlasí oblast materiálu a lokality.")

    def save(self, *args, **kwargs):
        self.region = self.location.region

        if self.operation == self.RECEIVED:
            self.quantity = abs(self.quantity)
        else:
            self.quantity = -abs(self.quantity)

        super().save(*args, **kwargs)


class Blacklist(models.Model):
    id_card_no = models.BigIntegerField("číslo průkazu", db_index=True)
    reason = models.TextField("zdůvodnění", null=True, blank=True)
