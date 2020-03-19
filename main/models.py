from django.conf import settings
from django.db import models


class Region(models.Model):
    ACTIVE = "active"
    DISABLED = "disabled"
    STATUS_CHOICES = [
        (ACTIVE, "aktivní"),
        (DISABLED, "pozastaven"),
    ]

    name = models.CharField("název", max_length=1000)
    about = models.TextField("popis", null=True, blank=True)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=ACTIVE, db_index=True
    )
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, through="RegionAdmin",)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RegionAdmin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.user.is_staff is False:
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)


class Material(models.Model):
    ACTIVE = "active"
    DISABLED = "disabled"
    STATUS_CHOICES = [
        (ACTIVE, "k dispozici"),
        (DISABLED, "blokován"),
    ]

    name = models.CharField("název", max_length=1000)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=ACTIVE, db_index=True
    )
    limit = models.FloatField("limit výdeje", null=True, blank=True)
    period = models.PositiveIntegerField("perioda výdeje", null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    ACTIVE = "active"
    DISABLED = "disabled"
    STATUS_CHOICES = [
        (ACTIVE, "aktivní"),
        (DISABLED, "pozastavena"),
    ]

    name = models.CharField("název", max_length=1000)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=ACTIVE, db_index=True
    )
    about = models.TextField("popis", null=True, blank=True)
    address = models.TextField("adresa", null=True, blank=True)
    phone = models.CharField("telefon", max_length=20)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL, through="LocationStaff",)

    class Meta:
        ordering = ["region", "name"]

    def __str__(self):
        return f"{self.region} - {self.name}"


class LocationStaff(models.Model):
    PENDING = "pending"
    ADMIN = "admin"
    VOLUNTEER = "volunteer"
    STATUS_CHOICES = [
        (PENDING, "čekatel"),
        (ADMIN, "správce"),
        (VOLUNTEER, "dobrovolník"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=PENDING
    )

    def save(self, *args, **kwargs):
        if self.status == self.ADMIN and self.user.is_staff is False:
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)


class Dispensed(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    quantity = models.IntegerField("množství")
    created = models.DateTimeField("vytvořeno", auto_now_add=True)
    changed = models.DateTimeField("upraveno", auto_now=True)
    id_card_no = models.CharField("číslo průkazu", max_length=100, db_index=True)

    class Meta:
        ordering = ["created"]


class MaterialRecord(models.Model):
    RECEIVED = "received"
    RETURNED = "returned"
    DISPENSED = "dispensed"
    OPERATION_CHOICES = [
        (RECEIVED, "přijetí"),
        (RETURNED, "vrácení"),
        (DISPENSED, "výdej"),
    ]

    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    quantity = models.IntegerField("množství")
    date = models.DateTimeField("datum", auto_now_add=True)
    operation = models.CharField(
        "operace", max_length=10, choices=OPERATION_CHOICES, db_index=True
    )

    class Meta:
        ordering = ["date"]
