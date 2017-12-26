from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def yamaps(raw_address, style="width: 480px; height: 320px;"):
    return mark_safe('<div class="django-yamaps" data-raw-address="{}" style="{}"></div>'.format(raw_address, style))


@register.simple_tag
def yamaps_init():
    lang = "ru-RU"
    if settings.LANGUAGE_CODE:
        lang = settings.LANGUAGE_CODE
    yamaps_js = '<script type="text/javascript" src="https://api-maps.yandex.ru/2.1/?lang={}"></script>' \
        .format(lang)
    return mark_safe(yamaps_js + '''
    <script type="text/javascript">
    window.onload = function() {
        ymaps.ready(function () {
            window.django_yamaps = [];

            var maps = document.querySelectorAll(".django-yamaps");
            maps.forEach(function (elem) {
                var map = new ymaps.Map(elem, {
                    center: [53.758768, 87.136731],
                    zoom: 15
                });
                var addr = elem.getAttribute("data-raw-address");
                ymaps.geocode(addr, { results: 1 }).then(function (res) {
                    var firstGeoObject = res.geoObjects.get(0),
                        coords = firstGeoObject.geometry.getCoordinates();
                    map.geoObjects.add(firstGeoObject);
                    map.setCenter(coords);
                });
                
                window.django_yamaps.push(map);
            });
    })};
    </script>''')
