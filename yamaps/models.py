from django.db import models


class AddressPart(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Country(AddressPart):
    pass

    class Meta:
        verbose_name_plural = "Countries"


class AdministrativeArea(AddressPart):
    country = models.ForeignKey(Country)

    def __str__(self):
        return "{}, {}".format(str(self.country), self.name)


class Locality(AddressPart):
    admin_area = models.ForeignKey(AdministrativeArea)

    def __str__(self):
        return "{}, {}".format(str(self.admin_area), self.name)

    class Meta:
        verbose_name_plural = "Localities"


class Street(AddressPart):
    locality = models.ForeignKey(Locality)

    def __str__(self):
        return "{}, {}".format(str(self.locality), self.name)


class AddressManager(models.Manager):

    def create_from_dict(self, data):
        country, _ = Country.objects.get_or_create(name=data.get("country"))

        admin_area, _ = AdministrativeArea\
            .objects\
            .get_or_create(
                name=data.get("admin_area"),
                country=country
            )

        locality, _ = Locality\
            .objects\
            .get_or_create(
                name=data.get("locality"),
                admin_area=admin_area
            )

        street, _ = Street.objects.get_or_create(
            name=data.get("street"),
            locality=locality
        )
        addr, _ = self.get_or_create(
            raw=data.get("raw"),
            street=street,
            house=data.get("house"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude")
        )
        return addr


class Address(models.Model):
    raw = models.CharField(max_length=300)
    street = models.ForeignKey(Street)
    house = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    objects = AddressManager()

    def as_dict(self):

        return {
            "raw": self.raw,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "country": self.street.locality.admin_area.country.name,
            "admin_area": self.street.locality.admin_area.name,
            "locality": self.street.locality.name,
            "street": self.street.name,
            "house": self.house,
        }

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.raw
