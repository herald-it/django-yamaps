(function () {
    function setAddress(input_name, geobj, raw) {
        var coords = geobj.geometry.getCoordinates();
        var addrDetails = geobj.properties.get("metaDataProperty.GeocoderMetaData.AddressDetails");

        addrDetails.latitude = coords[0];
        addrDetails.longitude = coords[1];

        var selector = 'input[name="' + input_name + '_json"]';
        var jsonInput = document.querySelector(selector);

        jsonInput.setAttribute("value", JSON.stringify(addrDetails));

        var raw_address = geobj.properties.get("text");
        raw.setAttribute("value", raw_address);
        raw.setAttribute("size", raw_address.length);
    }

    function setAddressFromCoords(coords, name, raw) {
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            setAddress(name, firstGeoObject, raw);
        });
    }

    function init() {
        var addrInputs = document.querySelectorAll("input.yamaps");

        [].forEach.call(addrInputs, function (elem) {
            var name = elem.getAttribute("name");
            var raw = document.querySelector('input[name="' + name + '"]');

            var map = new ymaps.Map(name + "_map", {
                center: [53.758768, 87.136731],
                zoom: 12,
                controls: ["zoomControl", "fullscreenControl", "searchControl"]
            });

            var searchControl = map.controls.get("searchControl");
            searchControl.events.add("resultselect", function (e) {
                var index = e.get("index");
                searchControl.getResult(index).then(function (val) {
                    setAddress(name, val, raw);
                });
            }, this);

            // Make search based on addr loaded from db (if any).
            var initial_data = raw.getAttribute("value");
            if (initial_data) {
                searchControl.search(initial_data);
            }

            // Click processing.
            var placemark;
            map.events.add('click', function (e) {
                var coords = e.get('coords');

                if (placemark) {
                    placemark.geometry.setCoordinates(coords);
                }
                else {
                    placemark = new ymaps.Placemark(coords, {}, {
                        preset: 'islands#violetDotIconWithCaption',
                        draggable: true
                    });
                    map.geoObjects.add(placemark);

                    placemark.events.add('dragend', function () {
                        setAddressFromCoords(placemark.geometry.getCoordinates(), name);
                    });
                }

                setAddressFromCoords(coords, name, raw);
            });
        });
    }
    ymaps.ready(init);
})();