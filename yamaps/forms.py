from decimal import Decimal

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import Address


def get_address_js():
    lang = "ru-RU"
    if settings.LANGUAGE_CODE:
        lang = settings.LANGUAGE_CODE
    yamaps_js_url = \
        "https://api-maps.yandex.ru/2.1/?lang={}".format(lang)
    return yamaps_js_url, "yamaps/js/yamaps-widget.js"


class AddressWidget(forms.TextInput):

    parts = ["latitude", "longitude", "country",
             "admin_area", "locality", "street", "house"]

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        classes = attrs.get('class', '')
        classes += (' ' if classes else '') + 'yamaps'
        attrs['class'] = classes
        kwargs['attrs'] = attrs
        super(AddressWidget, self).__init__(*args, **kwargs)

    def _media(self):
        return forms.Media(js=get_address_js())

    media = property(_media)

    def render(self, name, value, attrs=None, **kwargs):

        addr = {}
        if isinstance(value, Address):
            addr = value.as_dict()
        elif isinstance(value, int):
            addr = Address.objects.get(pk=value).as_dict()

        # Raw address input will be readonly.
        if "readonly" not in attrs:
            attrs["readonly"] = "readonly"

        elems = [super(AddressWidget, self)
                 .render(name, addr.get("raw", ""), attrs, **kwargs)]

        # Hidden address parts.
        elems.append('<div id="{}_components">'.format(name))

        for part in self.parts:
            elems.append(
                '<input type="hidden" name="{}_{}" value="{}" />'.format(
                    name, part, addr.get(part, "")
                ))

        elems.append("</div>")

        # Yandex map.
        elems.append('<div id="{}_map" style="width: 700px; height: 500px;"></div>'
                     .format(name))

        return mark_safe('\n'.join(elems))

    def value_from_datadict(self, data, files, name):
        raw = data.get(name, None)
        if not raw:
            return raw

        addr = {p: data.get("{}_{}".format(name, p)) for p in self.parts}
        addr["raw"] = raw
        return addr


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
