from django.db import models


class ExampleModel(models.Model):
    address = models.ForeignKey("Address")


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
        raw_country = data["Country"]
        country, _ = Country.objects.get_or_create(name=raw_country["CountryName"])

        raw_admin_area = raw_country["AdministrativeArea"]
        admin_area, _ = AdministrativeArea \
            .objects \
            .get_or_create(name=raw_admin_area["AdministrativeAreaName"], country=country)

        raw_locality = raw_admin_area["SubAdministrativeArea"]["Locality"]
        locality, _ = Locality \
            .objects \
            .get_or_create(name=raw_locality["LocalityName"], admin_area=admin_area)

        raw_street = raw_locality["Thoroughfare"]
        street, _ = Street.objects.get_or_create(name=raw_street["ThoroughfareName"], locality=locality)

        house = raw_street["Premise"]["PremiseNumber"]

        addr, _ = self.get_or_create(
            raw=data.get("raw"),
            street=street,
            house=house,
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

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.raw
