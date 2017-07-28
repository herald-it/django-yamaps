import json

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.apps import apps


from .settings import YAMAPS_ADDRESS_MODEL


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
        lang = "ru-RU"
        if settings.LANGUAGE_CODE:
            lang = settings.LANGUAGE_CODE
        yamaps_js_url = \
            "https://api-maps.yandex.ru/2.1/?lang={}".format(lang)
        return forms.Media(js=(yamaps_js_url, "yamaps/js/yamaps-widget.js"))

    media = property(_media)

    def render(self, name, value, attrs=None, **kwargs):
        # Raw address input will be readonly.
        if "readonly" not in attrs:
            attrs["readonly"] = "readonly"

        raw_address = ""

        if isinstance(value, int):
            addr_model = apps.get_model(YAMAPS_ADDRESS_MODEL)
            value = addr_model.objects.get(pk=value)
            try:
                raw_address = value.to_raw()
            except AttributeError:
                raw_address = str(value)

        text_input = super().render(name, raw_address, attrs, **kwargs)

        widget = """{old}
<div id="{name}_components">
<input type="hidden" name="{name}_json"/>
<div id="{name}_map" style="width: 700px; height: 500px;"></div>
</div>
        """.format(old=text_input, name=name)

        return mark_safe(widget)

    def value_from_datadict(self, data, files, name):
        raw = data.get(name, None)
        if not raw:
            return raw

        addr_json = data.get("{}_json".format(name))
        addr = json.loads(addr_json)
        addr["raw"] = raw
        return addr
