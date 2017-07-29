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
    yamaps_js = '<script type="text/javascript" src="https://api-maps.yandex.ru/2.1/?lang={}"></script>'\
        .format(lang)
    return mark_safe(yamaps_js + '''
    <script type="text/javascript">
    ymaps.ready(function () {
        var maps = document.querySelectorAll(".django-yamaps");
        [].forEach.call(maps, function (elem) {
            var map = new ymaps.Map(elem, {
                center: [53.758768, 87.136731],
                controls: ["zoomControl", "fullscreenControl", "searchControl"]
            });
            var addr = elem.getAttribute("data-raw-address");
            var searchControl = map.controls.get("searchControl");
            searchControl.search(addr);            
        });
    });
    </script>''')
