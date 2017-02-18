var map = Array.prototype.map;
baseMarkerGroup = new L.LayerGroup();
var mymap = L.map('mapid').setView([39.464559, -76.117401], 12);
L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}').addTo(mymap);
mymap.on('click', addReceiver);

var iconType1 = L.icon({
    iconUrl: 'static/starIcon.png',
    iconSize: [32, 32],
});

var popup = L.popup();

var ipTarget = location.host
// for laptop, uncomment below
//ipTarget = "localhost"

var newReceiver = null;
var receiverLon =  39.464559; //default
var receiverLat = -76.117401; //default

function addMarker(e){
    var clickLat = e.latlng.lat;
    var clickLOn = e.latlng.lng;
    if(addMarker != null){
	newMarker.remove();
	console.log("Removing old marker");
    }
    //$.get('http://' + ipTarget + ':5000/data?longitude=' + clickLng + '&latitude=' + clickLat, (data) => {
    //	newMarker = L.marker(e.latlng, {icon:iconType1}).addTo(mymap)
    //        .bindPopup("Latitude: " + String(e.latlng.lat.toFixed(6)) + "<br>" + "Longitude: " + String(e.latlng.lng.toFixed(6)) + "<br>" +
    //                   "Elevation: " + String(data.elevation.toFixed(2)) + "<br>" + "No. Visible Satellites: " + String(data.numberVisibleSatellites) +
    //	 	       "<br>" + "Constellation Quality: " + String(data.constellationQuality.toFixed(3))).openPopup();
	// console.log(data);
	//result = data.satelliteDetails;
	//var satAlt = map.call(result, (v) => (v.satAlt));
	//      document.getElementById("demo").innerHTML = sat_alt;
	// console.log(satAlt);
	//	  onMapClick(e, data);
  //});
  //  console.log(clickLat);
  //  console.log(clickLng);
    mymap.panTo(new L.LatLng(clickLat, clickLng));
}


function addReceiver(e){
    receiverLat = e.latlng.lat;
    receiverLon = e.latlng.lng;
    if(newReceiver != null){
	newReceiver.remove();
	console.log("Removing old receiver");
    }
    onMapClick(e);
    newReceiver = L.marker(e.latlng, {icon:iconType1}).addTo(mymap)
//    $.get('http://' + ipTarget + ':5000/data?longitude=' + clickLng + '&latitude=' + clickLat, (data) => {
//	newReceiver = L.marker(e.latlng, {icon:iconType1}).addTo(mymap)
//            .bindPopup("Latitude: " + String(e.latlng.lat.toFixed(6)) + "<br>" + "Longitude: " + String(e.latlng.lng.toFixed(6)) + "<br>" +
//                       "Elevation: " + String(data.elevation.toFixed(2)) + "<br>" + "No. Visible Satellites: " + String(data.numberVisibleSatellites) +
//		       "<br>" + "Constellation Quality: " + String(data.constellationQuality.toFixed(3))).openPopup();
	// console.log(data);
//	result = data.satelliteDetails;
//	var satAlt = map.call(result, (v) => (v.satAlt));
	//      document.getElementById("demo").innerHTML = sat_alt;
	// console.log(satAlt);
	//	  onMapClick(e, data);
//  });
//    console.log(clickLat);
//    console.log(clickLng);
    mymap.panTo(new L.LatLng(receiverLat, receiverLon));
}


function goto(){
    var longitude = document.getElementById('longitude').value;
    var latitude  = document.getElementById('latitude').value;
    mymap.panTo(new L.LatLng(latitude, longitude));
    mymap.setZoom(10);
}


function run(){
    console.log(receiverLat);
    $.get('http://' + ipTarget + ':5000/data?longitude=' + receiverLon + '&latitude=' + receiverLat, (data) => {
	newReceiver.bindPopup("Latitude: " + String(receiverLat.toFixed(6)) + "<br>" + "Longitude: " + String(receiverLon.toFixed(6)) + "<br>" +
			       "Elevation: " + String(data.elevation.toFixed(2)) + "<br>" + "No. Visible Satellites: " + String(data.numberVisibleSatellites) +
			       "<br>" + "Constellation Quality: " + String(data.constellationQuality.toFixed(3))).openPopup();
        console.log(data);
        result = data.satelliteDetails;
        var satAlt = map.call(result, (v) => (v.satAlt));
	//          document.getElementById("demo").innerHTML = sat_alt;
        console.log(satAlt);
    });
}


function onMapClick(e) {
  var clickLat = e.latlng.lat;
  var clickLng = e.latlng.lng;
  console.log(clickLat);
  console.log(clickLng);
//  popup
//      .setLatLng(e.latlng)
//      .setContent("Latitude: " + String(e.latlng.lat) + "<br>" + "Logintude: " + String(e.latlng.lng) + "<br>" +
//                  "Elevation: " + String(data.elevation) + "<br>" + "No. Visible Satellites: " + String(data.no_visible_satellites))
//    .openOn(mymap);
}
