
function initAutocomplete() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 47.156955, lng: 27.603038 },
    zoom: 13,
    mapTypeId: "roadmap",
  });
  const input = document.getElementById("pac-input");
  const button = document.getElementById("select-location-btn");
  const autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.bindTo("bounds", map);
  // Specify just the place data fields that you need.
  autocomplete.setFields(["place_id", "geometry", "name", "formatted_address"]);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(button);
  const infowindow = new google.maps.InfoWindow();
  const infowindowContent = document.getElementById("infowindow-content");
  infowindow.setContent(infowindowContent);
  const geocoder = new google.maps.Geocoder();
  const marker = new google.maps.Marker({ map: map });
  input.style.display="inline";
  marker.addListener("click", () => {
    infowindow.open(map, marker);
  });
  autocomplete.addListener("place_changed", () => {
    infowindow.close();
    const place = autocomplete.getPlace();

    if (!place.place_id) {
      return;
    }
    geocoder.geocode({ placeId: place.place_id }, (results, status) => {
      if (status !== "OK" && results) {
        window.alert("Geocoder failed due to: " + status);
        return;
      }
      map.setZoom(11);
      map.setCenter(results[0].geometry.location);
      // Set the position of the marker using the place ID and location.
      marker.setPlace({
        placeId: place.place_id,
        location: results[0].geometry.location,
      });
      marker.setVisible(true);
      infowindowContent.children["place-name"].textContent = place.name;
      //infowindowContent.children["place-id"].textContent = place.place_id;
      console.log(results[0]['address_components'] );
      let x=results[0]['address_components'];
      const equals = (a, b) =>
      a.length === b.length &&
      a.every((v, i) => v === b[i]);
      for (let i = 0; i < x.length; i++) {
          if(equals(["country", "political"],x[i]['types']))
          {
            document.cookie = "country="+x[i]['long_name'].toLowerCase()+";";
            break;
          }
      }
      infowindowContent.children["place-address"].textContent =
        results[0].formatted_address;
      infowindow.open(map, marker);
      button.style.display="inline";
    });
  });
}
