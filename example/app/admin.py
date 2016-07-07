from django.contrib import admin
from django import forms

from yamaps.forms import AddressField
from yamaps.forms import get_address_js

from .models import ExampleModel


class ExampleModelForm(forms.ModelForm):
    address = AddressField()

    class Meta:
        model = ExampleModel
        fields = "__all__"

    class Media:
        js = get_address_js()


@admin.register(ExampleModel)
class ExampleModelAdmin(admin.ModelAdmin):
    form = ExampleModelForm
