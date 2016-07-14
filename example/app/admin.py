from django.contrib import admin
from django import forms

from yamaps.forms import AddressField

from .models import ExampleModel


class ExampleModelForm(forms.ModelForm):
    address = AddressField()

    class Meta:
        model = ExampleModel
        fields = "__all__"


@admin.register(ExampleModel)
class ExampleModelAdmin(admin.ModelAdmin):
    form = ExampleModelForm
