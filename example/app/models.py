from django.db import models

from yamaps.models import Address


class ExampleModel(models.Model):
    address = models.ForeignKey(Address)
