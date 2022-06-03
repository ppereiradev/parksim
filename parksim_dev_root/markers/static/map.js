const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const map = L.map('map');
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);
const markers = JSON.parse(document.getElementById('markers-data').textContent);
//let feature = L.geoJSON(markers).bindPopup(function (layer) { return layer.feature.properties.name + "</br>Vagas: " + layer.feature.properties.parkspace; }).addTo(map);
let feature = L.geoJSON(markers,  {
    pointToLayer: function(feature, latlng) {
        return L.marker(latlng, {
          icon: new L.AwesomeNumberMarkers({
            number: feature.properties.parkspace,
            //markerColor: 'purple',
          }),
        });
    }
  }).bindPopup(function (layer) { return layer.feature.properties.name + "</br>Vagas: " + layer.feature.properties.parkspace; }).addTo(map);


map.fitBounds(feature.getBounds(), { padding: [100, 100] });

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);