(function () {
    function setAddress(input_name, geobj, raw) {


        var coords = geobj.geometry.getCoordinates();
        var addrDetails = geobj.properties.get("metaDataProperty.GeocoderMetaData.AddressDetails");

        var countryName = addrDetails.Country.CountryName;
        var adminAreaName = addrDetails.Country.AdministrativeArea.AdministrativeAreaName;
        var localityName = addrDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName;
        var streetName = addrDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.Thoroughfare.ThoroughfareName;
        var houseNumber = addrDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.Thoroughfare.Premise.PremiseNumber;

        var parts = {
            "latitude": coords[0],
            "longitude": coords[1],
            "country": countryName,
            "admin_area": adminAreaName,
            "locality": localityName,
            "street": streetName,
            "house": houseNumber
        };

        for (var property in parts) {
            if (parts.hasOwnProperty(property)) {
                var input = document.querySelector(
                    'input[name="' + input_name + 
                    "_" + property.toString() + '"]'
                );
                input.setAttribute("value", parts[property]);
            }
        }
 
        if (parts) {
            raw.setAttribute("value", geobj.properties.get("text"));
            resizeRawAddressInput(raw);
        }
    }

    function updateAddress(coords, name, raw) {
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            setAddress(name, firstGeoObject, raw);
        });
    }

    function resizeRawAddressInput(input) {
        input.setAttribute("size", input.getAttribute("value").length);
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
                        updateAddress(placemark.geometry.getCoordinates(), name);
                    });
                }
                updateAddress(coords, name, raw);
            });
        });
    }

    ymaps.ready(init);
})();