from django.contrib import admin
from django import forms

from .forms import AddressField

from .models import Country
from .models import AdministrativeArea
from .models import Locality
from .models import Street
from .models import Address

from .models import ExampleModel


admin.site.register(Country)
admin.site.register(AdministrativeArea)
admin.site.register(Locality)
admin.site.register(Street)
admin.site.register(Address)


class ExampleModelForm(forms.ModelForm):
    address = AddressField()

    class Meta:
        model = ExampleModel
        fields = "__all__"


@admin.register(ExampleModel)
class ExampleModelAdmin(admin.ModelAdmin):
    form = ExampleModelForm
