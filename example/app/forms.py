from decimal import Decimal

from django import forms

from yamaps.forms import AddressWidget

from .models import Address


class AddressField(forms.Field):
    widget = AddressWidget

    def to_python(self, value):

        if value is None or value == "":
            return None

        for field in ["latitude", "longitude"]:
            if field in value:
                if value[field]:
                    try:
                        value[field] = Decimal(value[field])
                    except:
                        raise forms.ValidationError(
                            "Invalid value for %(field)s",
                            code="invalid",
                            params={"field": field}
                        )
                else:
                    raise forms.ValidationError(
                        "Field %(field)s is required",
                        code="invalid",
                        params={"field": field}
                    )

        return Address.objects.create_from_dict(value)
