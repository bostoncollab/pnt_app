var map = Array.prototype.map;
baseMarkerGroup = new L.LayerGroup();
var mymap = L.map('mapid').setView([39.464559, -76.117401], 12);
L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}').addTo(mymap);
mymap.on('click', addMarker);

var iconType1 = L.icon({
    iconUrl: 'static/starIcon.png',
    iconSize: [32, 32],
});

var ipTarget = location.host

var newMarker = null;

function addMarker(e){
  var clickLat = e.latlng.lat;
  var clickLng = e.latlng.lng;
  $.get('http://' + ipTarget + ':5000/data?longitude=' + clickLng + '&latitude=' + clickLat, (data) => {
if(newMarker != null){
  newMarker.remove();
  console.log("Removing");
}
var newMarker = L.marker(e.latlng, {icon:iconType1}).addTo(mymap)
                .bindPopup("Latitude: " + String(e.latlng.lat.toFixed(6)) + "<br>" + "Longitude: " + String(e.latlng.lng.toFixed(6)) + "<br>" +
                    "Elevation: " + String(data.elevation.toFixed(2)) + "<br>" + "No. Visible Satellites: " + String(data.numberVisibleSatellites) + "<br>" + "Constellation Quality: " + String(data.constellationQuality.toFixed(3))).openPopup();
      console.log(data);
      result = data.satelliteDetails;
      var satAlt = map.call(result, (v) => (v.satAlt));
//      document.getElementById("demo").innerHTML = sat_alt;
      console.log(satAlt);
//	  onMapClick(e, data);
  });
  console.log(clickLat);
  console.log(clickLng);
  mymap.panTo(new L.LatLng(clickLat, clickLng));
}

var popup = L.popup();

function onMapClick(e, data) {
  var clickLat = e.latlng.lat;
  var clickLng = e.latlng.lng;
  console.log(clickLat);
  console.log(clickLng);
//  popup
//	.setLatLng(e.latlng)
//	.setContent("Latitude: " + String(e.latlng.lat) + "<br>" + "Logintude: " + String(e.latlng.lng) + "<br>" +
//	            "Elevation: " + String(data.elevation) + "<br>" + "No. Visible Satellites: " + String(data.no_visible_satellites))
//    .openOn(mymap);
}

function render(){
      var longitude = document.getElementById('longitude').value;
      var latitude = document.getElementById('latitude').value;
      mymap.panTo(new L.LatLng(latitude, longitude));
      mymap.setZoom(10);

      $.get('http://' + ipTarget + '5000/data?longitude=' + longitude + '&latitude=' + latitude, (data) => {
          console.log(data);
          result = data.satelliteDetails;
          var satAlt = map.call(result, (v) => (v.satAlt));
//          document.getElementById("demo").innerHTML = sat_alt;
          console.log(satAlt);
    });
}
