from django.contrib import admin

from .models import Country
from .models import AdministrativeArea
from .models import Locality
from .models import Street
from .models import Address


admin.site.register(Country)
admin.site.register(AdministrativeArea)
admin.site.register(Locality)
admin.site.register(Street)
admin.site.register(Address)
